import pickle


class Client:
    def __init__(self, database, minBufferSize, host, port, s, keysDir, wallet):
        self.database = database
        self.minBufferSize = minBufferSize
        self.host = host
        self.port = port
        self.socket = s
        self.keysDir = keysDir
        self.wallet = wallet

    def start(self):
        self.connect()
        self.identify()
        self.updateDatabase()

    def connect(self):
        # Connecting to the server
        print(f"[+] Connecting to {self.host}:{self.port}")
        self.socket.connect((self.host, self.port))
        print("[+] Connected.")

    def identify(self):
        length = str(len(self.wallet.address))
        self.socket.send(self.toMinSize(length).encode())
        self.socket.send(self.wallet.address.encode())

    def updateDatabase(self):
        tableNames = ["Blocks", "Transactions", "Unconfirmed_Transactions", "UTXO"]
        for tableName in tableNames:
            if tableName == "Blocks" or tableName == "Transactions":
                lastId = int(self.socket.recv(self.minBufferSize))
                m = self.database.getLastObjectId(tableName)
                self.socket.send(str(m).encode())

                for i in range(m + 1, lastId + 1):
                    length = int(self.socket.recv(self.minBufferSize).decode().strip())
                    object = pickle.loads(self.socket.recv(length))
                    self.database.addObject(self.database.rawToObject(tableName, object), True)
            else:
                length = int(self.socket.recv(self.minBufferSize))
                set1 = pickle.loads(self.socket.recv(length))

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
        tx = self.wallet.constructTx(transactionSender, transactionReceiver, int(transactionAmount))
        if tx is not None:
            pickledTx = pickle.dumps(tx)
            self.socket.send(self.toMinSize("2").encode())

            length = str(len(pickledTx))
            self.socket.send(self.toMinSize(length).encode())
            self.socket.send(pickledTx)

            res = self.socket.recv(self.minBufferSize).strip().decode()
            if res == "100":
                self.database.addObject(tx)
                for input in tx.inputs:
                    self.database.removeObject(self.database.getUtxoByScript(input.lockingScript))
            return True
        else:
            return None

    def blockInfo(self):
        self.socket.send(b"00001")
        length = int(self.socket.recv(self.minBufferSize))
        if length == 0:
            return 0
        else:
            block = pickle.loads(self.socket.recv(length))
            return block

    def mine(self, block):
        self.socket.send(b"00001")
        block.mine(self.wallet)
        length = str(len(pickle.dumps(block)))
        self.socket.send(self.toMinSize(length).encode())
        self.socket.send(pickle.dumps(block))
        if int(self.socket.recv(self.minBufferSize).decode().strip()) == 100:
            self.database.addObject(block)
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

    def toMinSize(self, string):
        while len(string) < self.minBufferSize:
            string += " "
        return string

    def close(self):
        self.socket.send(self.toMinSize("3").encode())
        self.socket.close()
