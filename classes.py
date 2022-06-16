import pickle
import time
from hashlib import sha256
from ecdsa import SigningKey, VerifyingKey
import KeysGeneration


# Block Class with it's basic attributes
# We have the block's index, transaction (between nodes) , timestamp (when it was created)
# the hash of the previous block and the nonce (number used once)
class Block:
    def __init__(self, index, transactions, timestamp, previousHash, blockHash, reward, nonce, difficulty):
        self.id = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previousHash = previousHash
        self.hash = blockHash
        self.reward = reward
        self.nonce = nonce
        self.difficulty = difficulty
        self.objectDesc = ObjectDesc("Blocks",
                                     "(:id, :transactions, :timestamp, :previousHash, :hash, :reward, :nonce, :difficulty)",
                                     {}, "id", ["transactions"])
        self.objectDesc.setDatabaseValues(self.__dict__)

    def computeHash(self):
        # self.__dict__ => all attributes defined for the object Block
        blockString = pickle.dumps(self.__dict__)

        # sha256() => Hash it with sha256
        # hexdigest() => Returns the encoded data in hexadecimal format
        return (sha256(blockString)).hexdigest()

    def mine(self, wallet):
        self.transactions.append(wallet.constructCoinbaseTx(50, wallet.address, None))
        blockHash = self.computeHash()
        while not blockHash.startswith('0' * self.difficulty):
            self.nonce += 1
            blockHash = self.computeHash()
        self.hash = blockHash
        self.objectDesc.setDatabaseValues(self.__dict__)
        return blockHash

    def finalReward(self):
        for tx in self.transactions:
            self.reward += tx.fees


class Input:
    def __init__(self, value, address, prevTxId, lockingScript, scriptSig):
        self.value = value
        self.address = address
        self.prevTxId = prevTxId
        self.lockingScript = lockingScript
        self.scriptSig = scriptSig


class Output:
    def __init__(self, index, value, address, transactionId, lockingScript):
        self.id = index
        self.value = value
        self.address = address
        self.transactionId = transactionId
        self.lockingScript = lockingScript
        self.objectDesc = ObjectDesc("UTXO", "(:id, :value, :address, :transactionId, :lockingScript)",
                                     {}, "lockingScript", [])
        self.objectDesc.setDatabaseValues(self.__dict__)


# Transaction Class with it's basic attributes
# the transactions inputs and outputs
# the sender signature of the transaction and the transaction ids
class Transaction:
    def __init__(self, index=None, type=None, inputs=None, outputs=None, timestamp=time.time(), transactionId="",
                 fees=None):
        self.id = index
        self.type = type
        if inputs is None:
            inputs = []
        if outputs is None:
            outputs = []
        self.inputs = inputs
        self.outputs = outputs
        self.timestamp = timestamp
        self.transactionId = transactionId
        self.fees = fees
        self.objectDesc = ObjectDesc("Transactions",
                                     "(:id, :type, :inputs, :outputs, :timestamp, :transactionId, :fees)",
                                     {}, "transactionId", ["inputs", "outputs"])
        self.objectDesc.setDatabaseValues(self.__dict__)

    # Function that computes and sets the transaction's id
    def computeTxId(self):
        txId = ""
        for input in self.inputs:
            d = input.__dict__
            for attrib in d:
                txId += sha256(str(d[attrib]).encode()).hexdigest()
        txId += sha256(str(self.timestamp).encode()).hexdigest()
        self.transactionId = (sha256(txId.encode())).hexdigest()
        self.objectDesc.setDatabaseValues(self.__dict__)
        return self.transactionId

    def addInput(self, input):
        self.inputs.append(input)
        self.objectDesc.setDatabaseValues(self.__dict__)

    def addOutput(self, output):
        self.outputs.append(output)
        self.objectDesc.setDatabaseValues(self.__dict__)

    def calculateFees(self):
        self.fees = 0
        for input in self.inputs:
            self.fees += input.value * 0.01
        self.objectDesc.setDatabaseValues(self.__dict__)


class UnconfirmedTransaction(Transaction):
    def __init__(self, index=None, type=None, inputs=None, outputs=None, timestamp=time.time(), transactionId="",
                 fees=None):
        super().__init__(index, type, inputs, outputs, timestamp, transactionId, fees)
        self.objectDesc.databaseTableName = 'Unconfirmed_Transactions'


class ObjectDesc:
    def __init__(self, databaseTableName, databaseColumnNames, databaseValues, distinctAttrib, toPickleAttrib):
        self.databaseTableName = databaseTableName
        self.databaseColumnNames = databaseColumnNames
        self.databaseValues = databaseValues
        self.distinctAttrib = distinctAttrib
        self.toPickleAttrib = toPickleAttrib

    def setDatabaseValues(self, dict):
        for attrib in dict:
            if attrib != "objectDesc":
                self.databaseValues[attrib] = dict[attrib]


class Wallet:
    def __init__(self, database):
        try:
            self.address = KeysGeneration.getAddress()
        except FileNotFoundError:
            KeysGeneration.generate()
            self.address = KeysGeneration.getAddress()
        self.database = database
        self.pubkey = VerifyingKey.from_pem(open("Keys\\PublicKey.pem").read())
        self.privkey = SigningKey.from_pem(open("Keys\\PrivateKey.pem").read())
        self.amount = self.balance()

    def balance(self):
        self.amount = 0
        utxos = self.database.getUtxoList(self.address)
        if utxos:
            for i in range(0, len(utxos)):
                self.amount += float(utxos[i].value)
        return self.amount

    def constructTx(self, transactionSender, transactionReceiver, transactionAmount):
        # Checking of the sender has enough money or if the receiver address is valid
        if self.balance() < transactionAmount or len(transactionReceiver) != len(transactionSender):
            return None
        else:
            # Creating a UnconfirmedTransaction instance
            transaction = UnconfirmedTransaction(self.database.getLastObjectId("Unconfirmed_Transactions") + 1, 2)
            # Querying the UTXO table
            utxos = self.database.getUtxoList(self.address)
            transaction.addInput(self.outToIn(utxos[0]))
            s = 0

            # Converting UTXO'S to Inputs and adding them to the Transaction's Inputs List
            for utxo in transaction.inputs:
                s += utxo.value
                if s < transactionAmount:
                    transaction.addInput(self.outToIn(utxos[transaction.inputs.index(utxo) + 1]))

            txId = transaction.computeTxId()

            # Output to the receiver
            out1 = Output(self.database.getLastObjectId("UTXO") + 1, transactionAmount, transactionReceiver, txId, 0)
            transaction.addOutput(self.createOutScript(out1))

            # Output to the sender
            out2 = Output(self.database.getLastObjectId("UTXO") + 1, s - transactionAmount * 1.01, transactionSender,
                          txId, 0)
            transaction.addOutput(self.createOutScript(out2))

            transaction.calculateFees()
            transaction.objectDesc.setDatabaseValues(transaction.__dict__)
            return transaction

    def constructCoinbaseTx(self, amount, address, outScript):
        transaction = Transaction(self.database.getLastObjectId("Transactions") + 1, 1)
        transaction.computeTxId()
        out = Output(self.database.getLastObjectId("UTXO") + 1, amount, address, transaction.transactionId, outScript)
        transaction.addOutput(self.createOutScript(out))
        transaction.calculateFees()
        transaction.objectDesc.setDatabaseValues(transaction.__dict__)
        return transaction

    def sign(self, script):
        return self.privkey.sign(script)

    def outToIn(self, out):
        return Input(out.value, out.address, out.transactionId, out.lockingScript, self.sign(out.lockingScript))

    def createOutScript(self, out):
        SEPERATOR = "<SEPERATOR>".encode()
        outScript = self.pubkey.to_string() + SEPERATOR + str(
            out.value).encode() + SEPERATOR + out.address.encode() + SEPERATOR + str(
            out.transactionId).encode() + SEPERATOR + str(time.time()).encode()
        out.lockingScript = outScript
        out.objectDesc.setDatabaseValues(out.__dict__)
        return out

    def getPendingAmount(self, sender):
        return self.database.getPendingAmount(sender)


# Database Class that queries,adds,deletes and updates any data desired
# on our defined classes (Blocks,Nodes,Unconfirmed and Confirmed Transactions) in the database
class Database:
    def __init__(self, connection, cursor):
        self.conn = connection
        self.c = cursor

    # Function that gets last object id from the database
    def getLastObjectId(self, tableName):
        if self.emptyTable(tableName):
            return 0
        else:
            self.c.execute("SELECT max(id) FROM {}".format(tableName))
            return self.c.fetchall()[0][0]

    def getFirstObjectId(self, tableName):
        if self.emptyTable(tableName):
            return 0
        else:
            self.c.execute("SELECT min(id) FROM {}".format(tableName))
            return self.c.fetchall()[0][0]

    def emptyTable(self, tableName):
        self.c.execute("SELECT * FROM {};".format(tableName))
        if self.c.fetchall():
            return False
        else:
            return True

    # Function that gets the object by id from the database
    def getObjectById(self, tableName, index):
        if tableName == "Blocks":
            block = Block(*self.getRawObjectById(tableName, index))
            self.unpickleObjectAttrib(block)
            return block
        if tableName == "Transactions":
            tx = Transaction(*self.getRawObjectById(tableName, index))
            self.unpickleObjectAttrib(tx)
            return tx
        if tableName == "Unconfirmed_Transactions":
            tx = UnconfirmedTransaction(*self.getRawObjectById(tableName, index))
            self.unpickleObjectAttrib(tx)
            return tx
        if tableName == "UTXO":
            output = Output(*self.getRawObjectById(tableName, index))
            self.unpickleObjectAttrib(output)
            return output

    # Function that gets the object by id from the database
    def getRawObjectById(self, tableName, index):
        self.c.execute("SELECT * FROM {} WHERE id=:id".format(tableName), {'id': index})
        res = self.c.fetchall()
        if res:
            return res[0]
        else:
            return None

    @staticmethod
    def rawToObject(tableName, rawData):
        if tableName == "Blocks":
            block = Block(*rawData)
            return block
        if tableName == "Transactions":
            tx = Transaction(*rawData)
            return tx
        if tableName == "Unconfirmed_Transactions":
            tx = UnconfirmedTransaction(*rawData)
            return tx
        if tableName == "UTXO":
            print(rawData)
            output = Output(*rawData)
            return output

    def setObjectId(self, object):
        objectId = self.getLastObjectId(object.objectDesc.databaseTableName)
        object.id = objectId + 1
        object.objectDesc.databaseValues['id'] = object.id

    # Function that adds the designed object to the database
    def addObject(self, object, definitive=False):
        if not definitive:
            self.setObjectId(object)
        self.pickleObjectAttrib(object)
        with self.conn:
            self.c.execute(
                "INSERT INTO {} VALUES {}".format(object.objectDesc.databaseTableName,
                                                  object.objectDesc.databaseColumnNames),
                object.objectDesc.databaseValues)

    def removeObject(self, object):
        distAttrib = object.objectDesc.distinctAttrib
        self.c.execute(
            "DELETE FROM {0} WHERE {1}=:{1}".format(object.objectDesc.databaseTableName, distAttrib),
            {'{}'.format(distAttrib): object.objectDesc.databaseValues[distAttrib]})
        self.conn.commit()

    def getFirstObject(self, tableName):
        minId = self.getFirstObjectId(tableName)
        return self.getObjectById(tableName, minId)

    def getUtxoList(self, address):
        self.c.execute("SELECT * FROM UTXO WHERE address=:address", {'address': address})
        utxos = self.c.fetchall()
        utxoList = []
        if len(utxos) != 0:
            for i in range(0, len(utxos)):
                utxoList.append(Output(*utxos[i]))
        return utxoList

    def getUtxoByScript(self, lockingScript):
        self.c.execute("SELECT * FROM UTXO WHERE lockingScript=:lockingScript", {'lockingScript': lockingScript})
        utxoId = self.c.fetchall()[0][0]
        return self.getObjectById("UTXO", utxoId)

    def getTxByTxId(self, transactionId):
        try:
            self.c.execute("SELECT * FROM Transactions WHERE transactionId=:transactionId",
                           {'transactionId': transactionId})
            TxId = self.c.fetchall()[0][0]
            return self.getObjectById("Transactions", TxId)
        except IndexError:
            try:
                self.c.execute("SELECT * FROM Unconfirmed_Transactions WHERE transactionId=:transactionId",
                               {'transactionId': transactionId})
                TxId = self.c.fetchall()[0][0]
                return self.getObjectById("Unconfirmed_Transactions", TxId)
            except IndexError:
                return None

    def getObjectList(self, tableName):
        res = []
        self.c.execute("SELECT * FROM {}".format(tableName))
        for i in self.c.fetchall():
            res.append(self.getObjectById(tableName, i[0]))
        return res

    def getObjectIdList(self, tableName):
        self.c.execute("SELECT id FROM {}".format(tableName))
        return self.c.fetchall()

    @staticmethod
    def pickleObjectAttrib(object):
        for attrib in object.objectDesc.toPickleAttrib:
            object.objectDesc.databaseValues[attrib] = pickle.dumps(object.objectDesc.databaseValues[attrib])

    @staticmethod
    def unpickleObjectAttrib(object):
        for attrib in object.objectDesc.toPickleAttrib:
            object.__dict__[attrib] = pickle.loads(object.objectDesc.databaseValues[attrib])

    def getPendingAmount(self, sender):
        pending = 0
        moneyIn = 0
        unconfTxList = self.getObjectList("Unconfirmed_Transactions")
        for unconfTx in unconfTxList:
            inputs = unconfTx.inputs
            outputs = unconfTx.outputs
            for input in inputs:
                if input.address == sender:
                    pending += input.value
            for output in outputs:
                if output.address == sender:
                    moneyIn += output.value
        return pending, moneyIn

    def search(self, param):
        try:
            p = int(param)
            try:
                return self.getObjectById("Blocks", p)
            except IndexError:
                return None
        except ValueError:
            return self.getTxByTxId(param)
