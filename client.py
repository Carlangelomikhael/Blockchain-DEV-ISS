import json
import pickle
import socket
import os
import argparse
from hashlib import sha256
import rsa
import sqlite3

# Parsing the node's username and password arguments passed in the CLI
parser = argparse.ArgumentParser(description='')
parser.add_argument('name', metavar='N', type=str)
parser.add_argument('password', metavar='N', type=str)
args = parser.parse_args()
vars_dict = vars(args)

# Connecting to existing database
conn = sqlite3.connect('test.db')

# The cursor allow us to execute SQL commands
c = conn.cursor()


# Block Class with it's basic attributes
# We have the block's index, transaction (between nodes) , timestamp (when it was created)
# the hash of the previous block and the nonce (number used once)
class Block:
    def __init__(self, index, transaction, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transaction = transaction
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    # Function that take as an input all the block's attributes
    # and outputs the hash of the block (encoded in sha256)
    def compute_hash(self):
        # json.dumps => Converts a Python object into a json string
        # self.__dict__ => all attributes defined for the object Block
        # json.dumps => Converts a Python object into a json string
        # self.__dict__ => all attributes defined for the object Block
        block_string = json.dumps(self.__dict__)

        # encode() => Encode the json string
        # sha256() => Hash it with sha256
        # hexdigest() => Returns the encoded data in hexadecimal format
        return (sha256(block_string.encode())).hexdigest()


# send/receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# The ip address or hostname of the server, the receiver
# If you are running the client script on another device use the ip address of the server
host = socket.gethostbyname(socket.gethostname())
# the port, let's use 5001
port = 5001

# create the client socket
s = socket.socket()

# Connecting to the server
print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")

# Getting the node's name and password from the CLI args
name = vars_dict['name']
password = vars_dict['password']


def get_unconf_tx():
    c.execute("SELECT * FROM Unconfirmed_Transactions LIMIT 1")
    return c.fetchall()


def login():
    # Sending the node's username and password to the server
    data_string = name + SEPARATOR + password
    s.send(data_string.encode())

    message = s.recv(BUFFER_SIZE).decode()
    print(message)
    if message == 'Logged in':
        # update_blockchain_copy()
        node_choice()


def update_blockchain_copy():
    message = s.recv(BUFFER_SIZE).decode()
    if message == 'Your blockchain copy is not up to date please specify the path where the copy is saved':

        print(message)

        s.send('done'.encode())
        message = s.recv(BUFFER_SIZE).decode()
        print(message)

    else:
        print(message)


def node_choice():
    # Receiving the services message and printing it
    # Taking the nodes choice
    message = s.recv(BUFFER_SIZE).decode()
    print(message)
    choice = input()

    try:
        int(choice)

        s.send(str(choice).encode())

        if int(choice) == 1:
            create_keys()
        elif int(choice) == 2:
            recv_block_data()
        else:
            close_connection()
    except:
        s.send(str(choice).encode())
        error = s.recv(BUFFER_SIZE).decode()
        print(error)
        node_choice()


def create_keys():
    response = s.recv(32).decode()
    if response == '1':
        # Generating a public and private key (1024 bits rsa keys are considered medium-strength keys)
        (pubkey, privkey) = rsa.newkeys(1024)

        # Setting the directory where the private key file will be saved
        # if the directory doesn't exist we create it and we save the private key in bytes format
        # The dumps() method of the Python pickle module serializes a python object
        directory = f'C:\\Users\\User\\Downloads\\{name}_private_key'
        filename = "PrivateKey.txt"
        file_path = os.path.join(directory, filename)
        if not os.path.isdir(directory):
            os.mkdir(directory)
        file = open(file_path, "wb")
        file.write(pickle.dumps(privkey))
        file.close()

        # Setting the directory where the public key file will be saved
        # same functionality as above
        directory = f'C:\\Users\\User\\Downloads\\{name}_public_key'
        filename = "PublicKey.txt"
        file_path = os.path.join(directory, filename)
        if not os.path.isdir(directory):
            os.mkdir(directory)
        file = open(file_path, "wb")
        file.write(pickle.dumps(pubkey))
        file.close()

        send_public_key(file_path)
    else:
        print(response)
        node_choice()


def send_public_key(file_path):
    # start sending the file
    with open(file_path, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transmission in
            # busy networks
            s.sendall(bytes_read)


def recv_block_data():
    message = s.recv(BUFFER_SIZE).decode()
    if message == 'No transactions to mine':
        print(message)
        node_choice()
    else:
        mine(message.split(SEPARATOR))


def mine(block_list):
    block_index, block_transaction, block_timestamp, block_previous_hash, block_nonce = block_list
    block = Block(block_index, block_transaction, block_timestamp, block_previous_hash, int(block_nonce))
    block_hash = block.compute_hash()

    while not block_hash.startswith('0' * 5):
        block.nonce += 1
        block_hash = block.compute_hash()

    s.send(block_hash.encode())
    node_choice()


def close_connection():
    s.close()


login()
