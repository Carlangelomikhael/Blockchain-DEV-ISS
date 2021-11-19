import json
import socket
from hashlib import sha256
import sqlite3
import time
from _thread import *
from app import Node, Transactions

# local host IP address
SERVER_HOST = "0.0.0.0"
# Port to listen on
SERVER_PORT = 5001
# send/receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# Connecting to existing database
conn = sqlite3.connect('test.db', check_same_thread=False)

# The cursor allow us to execute SQL commands
c = conn.cursor()

# create the server socket
# The arguments passed to socket() specify the address family and socket type.
# AF_INET is the Internet address family for IPv4.
# SOCK_STREAM is the socket type for TCP, the protocol that will be used to transport our messages in the network.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to our local address
# bind() is used to associate the socket with a specific network interface and port number
s.bind((SERVER_HOST, SERVER_PORT))

# enabling our server to accept connections
# 5 here is the number of unaccepted connections that
# the system will allow before refusing new connections
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")


def update_pubkey(node_id, pubkey):
    with conn:
        c.execute("""UPDATE Nodes SET pubkey = :pubkey
        WHERE node_id = :node_id""",
                  {'pubkey': pubkey, 'node_id': node_id})


def add_conf_tx(tx):
    with conn:
        c.execute(
            "INSERT INTO Transactions VALUES (:id, :inputs, :outputs, :signature, :transaction_id)",
            {'id': tx.id, 'inputs': tx.inputs, 'outputs': tx.outputs, 'signature': tx.signature,
             'transaction_id': tx.transaction_id})


def get_tx(transaction_id):
    c.execute("SELECT * FROM Transactions WHERE transaction_id=:transaction_id",
              {'transaction_id': transaction_id})
    t = c.fetchall()[0][1:]
    return Transactions(*t)


def get_last_tx_index():
    c.execute("SELECT * FROM Transactions ORDER BY ID DESC LIMIT 1")
    try:
        return c.fetchall()[0][4]
    except IndexError:
        return 0


def get_pending_amount(node_id):
    return get_node(node_id).pending_money_amount


def get_money(node_id):
    return get_node(node_id).money_amount


def update_money(tx):
    with conn:
        c.execute("""UPDATE Nodes SET pending_money_amount = :pending_money_amount
        WHERE node_id = :node_id""",
                  {'pending_money_amount': get_pending_amount(json.loads(tx.outputs)["sender"]) - 1.05 *
                                           json.loads(tx.outputs)["amount"],
                   'node_id': json.loads(tx.outputs)["sender"]})

        c.execute("""UPDATE Nodes SET money_amount = :money_amount
        WHERE node_id = :node_id""",
                  {'money_amount': get_money(json.loads(tx.outputs)["receiver"]) + json.loads(tx.outputs)["amount"],
                   'node_id': json.loads(tx.outputs)["receiver"]})

        c.execute("""UPDATE Nodes SET money_amount = :money_amount
        WHERE node_id = :node_id""",
                  {'money_amount': get_money(node_id) + 0.05 * json.loads(tx.outputs)["amount"], 'node_id': node_id})


def get_node(node_id):
    c.execute("SELECT * FROM Nodes WHERE node_id=:node_id", {'node_id': node_id})
    return Node(*c.fetchall()[0])


def get_unconf_tx():
    c.execute("SELECT * FROM Unconfirmed_Transactions LIMIT 1")
    try:
        t = c.fetchall()[0][1:]
        return Transactions(*t)
    except IndexError:
        return 0


def get_last_block():
    c.execute("SELECT * FROM Blocks ORDER BY ID DESC LIMIT 1")
    return c.fetchall()[0]


def insert_block(index, tx, timestamp, previous_hash, nonce, hash):
    with conn:
        c.execute(
            "INSERT INTO Blocks VALUES (:id, :index, :transactions, :timestamp, :previous_hash, :nonce, :hash)",
            {'id': index + 1, 'index': index, 'transactions': tx, 'timestamp': timestamp,
             'previous_hash': previous_hash, 'nonce': nonce, 'hash': hash})


def delete_conf_tx(transaction_id):
    with conn:
        c.execute("DELETE from Unconfirmed_Transactions WHERE transaction_id = :transaction_id",
                  {'transaction_id': transaction_id})
        conn.commit()


def login():
    if sha256(password.encode()).hexdigest() == node_data.password:
        # Logged in message sent to the node
        node_socket.send('Logged in'.encode())
        # check_blockchain_copy()
        choice()


def check_blockchain_copy():
    if node_data.newest_chain_copy == 0:
        message = 'Your blockchain copy is not up to date' \
                  ' please specify the path where the copy is saved'
        node_socket.send(message.encode())
        node_socket.recv(BUFFER_SIZE)

        message = 'Synchronising with latest version .... '
        node_socket.send(message.encode())
    else:
        node_socket.send('Your blockchain copy is up to date'.encode())


def choice():
    # Services message sent to the node
    message = 'What would you like to do?: \n' \
              '1- Set your Public Key \n' \
              '2- Mine new Blocks \n' \
              '3- Close Connection \n' \
              'Enter your Choice: '
    # Sending the message through the node socket
    node_socket.send(message.encode())

    # Checking if any data has been sent from the client
    # Waiting for client to send his choice
    data = node_socket.recv(32).decode()

    if int(data) == 1:
        set_public_key()
    elif int(data) == 2:
        mine()
    else:
        close_connection()


def set_public_key():
    if len(node_data.pubkey) != 0:
        node_socket.send('You can\'t change your public key'.encode())
        choice()
    else:
        node_socket.send('1'.encode())

    pubkey = b''

    # start receiving the public key and then adding it to the database
    while True:
        # read 1024 bytes from the socket (receive)
        bytes_read = node_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            # nothing is received
            # file transmitting is done
            break
        pubkey += bytes_read

    update_pubkey(node_id, pubkey)


def mine():
    if transaction:
        block_index = block[1] + 1
        block_transaction = transaction.transaction_id
        block_timestamp = time.time()
        block_previous_hash = block[4]
        block_nonce = 0

        block_data_list = [block_index, block_transaction, block_timestamp, block_previous_hash, block_nonce]
        block_data_string = b''

        for i in range(len(block_data_list)):
            if i != 4:
                try:
                    block_data_string += block_data_list[i].encode() + SEPARATOR.encode()
                except:
                    block_data_string += str(block_data_list[i]).encode() + SEPARATOR.encode()
            else:
                block_data_string += str(block_data_list[i]).encode()

        node_socket.send(block_data_string)
        block_hash = node_socket.recv(BUFFER_SIZE).decode()
        print(block_hash)

        insert_block(block_index, block_transaction, block_timestamp, block_previous_hash, block_nonce, block_hash)
        conf_tx = get_unconf_tx()
        add_conf_tx(conf_tx)
        delete_conf_tx(conf_tx.transaction_id)

        update_money(get_tx(block_transaction))

    else:
        node_socket.send('No transactions to mine'.encode())
        choice()


def close_connection():
    # close the client socket
    node_socket.close()


while True:
    node_socket, address = s.accept()

    # if below code is executed, that means the sender is connected
    print(f"[+] {address} is connected.")

    # Saving the name and password sent by the node
    node_id, password = node_socket.recv(BUFFER_SIZE).decode().split(SEPARATOR)

    # Querying the node from the database filtered by id
    node_data = get_node(node_id)

    # Querying the first Unconfirmed Transaction from the database
    transaction = get_unconf_tx()

    # Querying the Blocks table
    block = get_last_block()

    start_new_thread(login, ())

node_socket.close()
