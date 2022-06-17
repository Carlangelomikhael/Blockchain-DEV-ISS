import os
import pickle
import socket
import sqlite3
import time
from ecdsa import VerifyingKey, SECP256k1
import init_database
from classes import Block, Database, Transaction

# local host IP address
serverHost = socket.gethostbyname(socket.gethostname())
# Port to listen on
serverPort = 50000
# Minimum data size to be sent/received
minBufferSize = 5
# Seperator used by both parties to identify data
SEPERATOR = "<SEPERATOR>"

# Creates a database if non-existent
if not os.path.exists("database.db"):
    init_database.main("database.db")

# Connecting to existing database
conn = sqlite3.connect('database.db', check_same_thread=False)

# The cursor allow us to execute SQL commands
c = conn.cursor()

# Creating a Database instance
database = Database(conn, c)

# create the server socket
# The arguments passed to socket() specify the address family and socket type.
# AF_INET is the Internet address family for IPv4.
# SOCK_STREAM is the socket type for TCP, the protocol that will be used to transport our messages in the network.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to our local ip address on port 5001
# bind() is used to associate the socket with a specific network interface and port number
s.bind((serverHost, serverPort))

# enabling our server to accept connections
# 5 here is the number of unaccepted connections that
# the system will allow before refusing new connections
s.listen(5)
print(f"[*] Listening as {serverHost}:{serverPort}")


# Receive the node's wallet address
def nodeLogin():
    length = receive(minBufferSize, "Int")
    print(receive(length, "String"))


# Update the node's database if needed
def updateDatabase():
    # We got 4 tables in our database
    tableNames = ["Blocks", "Transactions", "Unconfirmed_Transactions", "UTXO"]
    for tableName in tableNames:
        # For the Blocks and Transactions tables it's enough to check what index is last in the node's database
        # Because no block or transaction will ever be deleted
        if tableName == "Blocks" or tableName == "Transactions":
            lastId = database.getLastObjectId(tableName)
            nodeSocket.send(toMinSize(toMinSize(str(lastId))).encode())
            m = receive(minBufferSize, "Int")
            for i in range(m + 1, lastId + 1):
                rawData = database.getRawObjectById(tableName, i)
                if rawData:
                    pickledObject = pickle.dumps(rawData)
                    length = len(pickledObject)
                    nodeSocket.send(toMinSize(str(length)).encode())
                    nodeSocket.send(pickledObject)

        # For the other tables we need to check what indexes are present in the node's and server's database
        # Then we compare the two resulting sets of indexes to see which objects are to be added/deleted
        else:
            set1 = pickle.dumps(set(database.getObjectIdList(tableName)))
            length = toMinSize(str(len(set1))).encode()
            nodeSocket.send(length)
            nodeSocket.send(set1)

            length = int(nodeSocket.recv(minBufferSize))
            set2 = pickle.loads(nodeSocket.recv(length))

            # Elements that are missing
            toAdd = pickle.loads(set1) - set2

            # Sending the elements that needs to be added
            for elmnt in toAdd:
                object = pickle.dumps(database.getObjectById(tableName, elmnt[0]))
                length = toMinSize(str(len(object))).encode()
                nodeSocket.send(length)
                nodeSocket.send(object)


def mine():
    # Sending info about the Genesis Block
    if database.emptyTable("Blocks"):
        block = Block(0, [], time.time(), "", "", 50, 0, 2)
        block.finalReward()
        length = toMinSize(str(len(pickle.dumps(block))))
        nodeSocket.send(length.encode())
        nodeSocket.send(pickle.dumps(block))
    else:
        # Sending info about the next Block
        if not database.emptyTable("Unconfirmed_Transactions"):
            tx = database.getFirstObject("Unconfirmed_Transactions")
            index = database.getLastObjectId("Blocks") + 1
            prevHash = database.getObjectById("Blocks", index - 1).hash
            block = Block(index,
                          [Transaction(tx.id, tx.type, tx.inputs, tx.outputs, tx.timestamp,
                                       tx.transactionId, tx.fees)], time.time(), prevHash, "0", 50, 0, 2)
            block.finalReward()
            length = toMinSize(str(len(pickle.dumps(block))))
            nodeSocket.send(length.encode())
            nodeSocket.send(pickle.dumps(block))
        else:
            # No Block available for mining
            msg = "0"
            nodeSocket.send(toMinSize(msg).encode())
            return False

    # Waiting to see if the node wants to mine the block
    request = receive(minBufferSize, "Int")
    # Receiving the block's hash then adding the Block to the database
    if request == 1:
        length = receive(minBufferSize, "Int")
        block = receive(length, "Object")
        database.addObject(block)
        nodeSocket.send(toMinSize("100").encode())
        # Adding the transactions that are in the block to the database
        for tx in block.transactions:
            database.addObject(tx)
            # If the transaction type is 2 it means that's a regular transaction from node to node
            # We remove it from the Unconfirmed_Transactions table and add the outputs that are in the tx
            if tx.type == 2:
                database.removeObject(database.getFirstObject("Unconfirmed_Transactions"))
                for output in tx.outputs:
                    database.addObject(output)
            # If the transaction type is 1 it means that's a transaction made to reward the miner for mining the block
            # Then w add the outputs that are in the tx
            elif tx.type == 1:
                for output in tx.outputs:
                    database.addObject(output)


# Function that is always listening to the node and acts depending on the request made
def waiting():
    request = receive(minBufferSize, "Int")
    if request is not None:
        if request == 1:
            mine()
            waiting()
        elif request == 2:
            transaction()
            waiting()
        else:
            close()


# Function that transform any given string which length is < to the minimum buffer size to the minimum size
def toMinSize(string):
    while len(string) < minBufferSize:
        string += " "
    return string


def transaction():
    # Receive Transaction from Node
    length = receive(minBufferSize, "Int")
    tx = receive(length, "Object")
    # Checking if the Transaction is valid
    valid = True
    for input in tx.inputs:
        if database.getUtxoByScript(input.lockingScript):
            lockingScript = input.lockingScript
            scriptSig = input.scriptSig
            data = lockingScript.split(SEPERATOR.encode())
            pubkey = VerifyingKey.from_string(data[0], curve=SECP256k1)

            pubkey.verify(scriptSig, lockingScript)
            database.removeObject(database.getUtxoByScript(input.lockingScript))
        else:
            valid = False

    # If the tx is valid we add it to the database and signal the node to do so
    if valid:
        database.addObject(tx)
        nodeSocket.send(toMinSize("100").encode())


# Function that closes the connection to the node
def close():
    nodeSocket.close()


# This function is made to be able to handle errors whilst receiving data from the node
# For example if we are receiving data and the node disconnects in the process the server won't crash
def receive(length, type):
    if type == "Object":
        try:
            try:
                object = pickle.loads(nodeSocket.recv(length))
            except:
                return None
            return object
        except (ConnectionResetError, OSError):
            close()
    if type == "Int":
        try:
            try:
                request = int(nodeSocket.recv(length))
            except TypeError:
                return None
            return request
        except (ConnectionResetError, OSError, ValueError):
            close()
    if type == "String":
        try:
            try:
                request = str(nodeSocket.recv(length).decode().strip())
            except TypeError:
                return None
            return request
        except (ConnectionResetError, OSError, ValueError):
            close()


# Loop that will keep the server going indefinitely and accept node connections
while True:
    nodeSocket, address = s.accept()

    # if below code is executed, that means the sender is connected
    print(f"[+] {address} is connected.")

    nodeLogin()
    updateDatabase()
    waiting()
