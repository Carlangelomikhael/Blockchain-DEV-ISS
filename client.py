import pickle


# Client Class with it's basic attributes
class Client:
    def __init__(self, database, minBufferSize, host, port, s, keysDir, wallet):
        self.database = database
        self.minBufferSize = minBufferSize
        self.host = host
        self.port = port
        self.socket = s
        self.keysDir = keysDir
        self.wallet = wallet

    # Function that starts the connection to the server
    def start(self):
        self.connect()
        self.identify()
        self.updateDatabase()

    def connect(self):
        # Connecting to the server
        print(f"[+] Connecting to {self.host}:{self.port}")
        self.socket.connect((self.host, self.port))
        print("[+] Connected.")

    # Sending our wallet address to the server
    def identify(self):
        length = str(len(self.wallet.address))
        self.socket.send(self.toMinSize(length).encode())
        self.socket.send(self.wallet.address.encode())

    def updateDatabase(self):
        tableNames = ["Blocks", "Transactions", "Unconfirmed_Transactions", "UTXO"]
        for tableName in tableNames:
            if tableName == "Blocks" or tableName == "Transactions":
                # Receiving the id of the last object in table
                lastId = int(self.socket.recv(self.minBufferSize))
                # Getting the id of the last object then sending it to the server
                m = self.database.getLastObjectId(tableName)
                self.socket.send(str(m).encode())

                # Receiving and adding the missing objects
                for i in range(m + 1, lastId + 1):
                    length = int(self.socket.recv(self.minBufferSize).decode().strip())
                    object = pickle.loads(self.socket.recv(length))
                    self.database.addObject(self.database.rawToObject(tableName, object), True)
            else:
                length = int(self.socket.recv(self.minBufferSize))
                # Receiving the set that contains the object ids from the server
                set1 = pickle.loads(self.socket.recv(length))

                # Sending the set that contains the object ids to the server
                set2 = pickle.dumps(set(self.database.getObjectIdList(tableName)))
                length = self.toMinSize(str(len(set2))).encode()
                self.socket.send(length)
                self.socket.send(set2)

                set2 = pickle.loads(set2)
                # Elements that are missing
                toAdd = set1 - set2

                if toAdd:
                    for i in range(0, len(toAdd)):
                        length = int(self.socket.recv(self.minBufferSize))
                        object = pickle.loads(self.socket.recv(length))
                        self.database.addObject(object, definitive=True)

                # Elements that are in excess
                toDelete = set2 - set1

                if toDelete:
                    for elmnt in toDelete:
                        self.database.removeObject(self.database.getObjectById(tableName, elmnt[0]))

    def transact(self, transactionSender, transactionReceiver, transactionAmount):
        # Constructing the transaction
        tx = self.wallet.constructTx(transactionSender, transactionReceiver, int(transactionAmount))
        if tx is not None:
            pickledTx = pickle.dumps(tx)
            # Signaling the server that there is a new issued transaction
            self.socket.send(self.toMinSize("2").encode())

            # Sending the transaction to the server
            length = str(len(pickledTx))
            self.socket.send(self.toMinSize(length).encode())
            self.socket.send(pickledTx)

            # Getting the confirmation from the server then adding the tx to the database
            # Removing all the spent UTXO'S from the database
            res = self.socket.recv(self.minBufferSize).strip().decode()
            if res == "100":
                self.database.addObject(tx)
                for input in tx.inputs:
                    self.database.removeObject(self.database.getUtxoByScript(input.lockingScript))
            return True
        else:
            return None

    # Function that requests the newest block info
    def blockInfo(self):
        self.socket.send(b"00001")
        length = int(self.socket.recv(self.minBufferSize))
        if length == 0:
            return 0
        else:
            block = pickle.loads(self.socket.recv(length))
            return block

    def mine(self, block):
        # Signaling the server that we are mining
        self.socket.send(b"00001")
        block.mine(self.wallet)
        # Sending the result block to the server
        length = str(len(pickle.dumps(block)))
        self.socket.send(self.toMinSize(length).encode())
        self.socket.send(pickle.dumps(block))
        # Receiving confirmation about the block then adding it to the database
        if int(self.socket.recv(self.minBufferSize).decode().strip()) == 100:
            self.database.addObject(block)
            # Removing every tx from the Unconfirmed_Transactions table to the Transactions table
            # And adding the txs outputs
            for tx in block.transactions:
                if tx.type == 2:
                    self.database.addObject(tx)
                    self.database.removeObject(self.database.getFirstObject("Unconfirmed_Transactions"))
                    for output in tx.outputs:
                        self.database.addObject(output)
                elif tx.type == 1:
                    self.database.addObject(tx)
                    for output in tx.outputs:
                        self.database.addObject(output)

    # Function that transform any given string which length is < to the minimum buffer size to the minimum size
    def toMinSize(self, string):
        while len(string) < self.minBufferSize:
            string += " "
        return string

    # Function that sends a "close" signal to the server
    def close(self):
        self.socket.send(self.toMinSize("3").encode())
        self.socket.close()
