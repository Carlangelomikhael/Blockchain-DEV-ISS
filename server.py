import socket
from hashlib import sha256
import sqlite3
import time
from _thread import *

# local host IP address
SERVER_HOST = "0.0.0.0"
# Port to listen on
SERVER_PORT = 5001
# send/receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# Connecting to existing database
conn = sqlite3.connect('database.db', check_same_thread=False)

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


def update_pubkey(name, pubkey):
    with conn:
        c.execute("""UPDATE Nodes SET pubkey = :pubkey
        WHERE name = :name""",
                  {'pubkey': pubkey, 'name': name})


def get_tx_id():
    c.execute("SELECT * FROM Unconfirmed_Transactions WHERE transaction_id=:transaction_id", {'transaction_id': name})
    return c.fetchall()


def update_money_sender():
    with conn:
        c.execute("""UPDATE Nodes SET pending_money_amount = :pending_money_amount
        WHERE name = :name""",
                  {'pending_money_amount': 0, 'name': name})


def get_node(name):
    c.execute("SELECT * FROM Nodes WHERE name=:name", {'name': name})
    return c.fetchall()


def get_unconf_tx():
    c.execute("SELECT * FROM Unconfirmed_Transactions LIMIT 1")
    return c.fetchall()


def get_last_block():
    c.execute("SELECT * FROM Blocks ORDER BY ID DESC LIMIT 1")
    return c.fetchall()


def insert_block(index, transaction, timestamp, previous_hash, nonce, hash):
    with conn:
        c.execute(
            "INSERT INTO Blocks VALUES (:id, :index, :transaction, :timestamp, :previous_hash, :nonce, :hash)",
            {'id': index - 1, 'index': index, 'transaction': transaction, 'timestamp': timestamp,
             'previous_hash': previous_hash, 'nonce': nonce, 'hash': hash})


def delete_conf_tx(id):
    with conn:
        c.execute("DELETE from Unconfirmed_Transactions WHERE id = :id",
                  {'id': id})


def login():
    if sha256(password.encode()).hexdigest() == node_data[0][5]:
        # Logged in message sent to the node
        node_socket.send('Logged in'.encode())
        check_blockchain_copy()
        choice()


def check_blockchain_copy():
    if node_data[0][6] == 0:
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
    if type(node_data[0][4]) == bytes:
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

    update_pubkey(name, pubkey)


def mine():
    if transaction:
        block_index = block[0][1] + 1
        block_transaction = transaction[0][1]
        block_timestamp = time.time()
        block_previous_hash = block[0][4]
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
        delete_conf_tx(conf_tx[0][0])

    else:
        node_socket.send('No transactions to mine'.encode())
        close_connection()


def close_connection():
    # close the client socket
    node_socket.close()
    # close the server socket
    s.close()


while True:
    node_socket, address = s.accept()

    # if below code is executed, that means the sender is connected
    print(f"[+] {address} is connected.")

    # Saving the name and password sent by the node
    name, password = node_socket.recv(BUFFER_SIZE).decode().split(SEPARATOR)

    node_data = get_node(name)

    # Querying the Unconfirmed Transactions table
    transaction = get_unconf_tx()

    # Querying the Blocks table
    block = get_last_block()

    start_new_thread(login, ())

node_socket.close()
