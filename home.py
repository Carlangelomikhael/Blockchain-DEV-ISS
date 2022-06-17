import datetime
import json
import os
import pickle
import socket
import sqlite3

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QWidget

from classes import Database, Wallet
from client import Client


class Ui_HomeWindow(object):
    def setupUi(self, HomeWindow):
        HomeWindow.setObjectName("HomeWindow")
        HomeWindow.setMinimumSize(QtCore.QSize(1500, 440))
        HomeWindow.setMaximumSize(QtCore.QSize(1500, 440))
        HomeWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        HomeWindow.setWindowFlags(Qt.FramelessWindowHint)
        self.centralwidget = QtWidgets.QWidget(HomeWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Connecting to existing database
        conn = sqlite3.connect('database.db', check_same_thread=False)

        # The cursor allow us to execute SQL commands
        c = conn.cursor()

        database = Database(conn, c)
        wallet = Wallet(database)

        minBufferSize = 5

        # The ip address or hostname of the server, the receiver
        # If you are running the client script on another device use the ip address of the server
        host = socket.gethostbyname(socket.gethostname())
        # the port, let's use 5001
        port = 50000

        # create the client socket
        s = socket.socket()

        keysDir = "C:{}\\Keys".format(os.getcwd())
        self.client = Client(database, minBufferSize, host, port, s, keysDir, wallet)

        # First frame title
        self.frame1_title = QtWidgets.QLabel(self.centralwidget)
        self.frame1_title.setGeometry(QtCore.QRect(14, 10, 60, 30))
        self.frame1_title.setStyleSheet("font: 75 12pt \"MS Shell Dlg 2\";")
        self.frame1_title.setObjectName("frame1_title")

        # Frame containing the wallet's address and balance
        self.frame1 = QtWidgets.QFrame(self.centralwidget)
        self.frame1.setGeometry(QtCore.QRect(10, 43, 720, 110))
        self.frame1.setStyleSheet("border: 2px solid rgb(208, 83, 64);")
        self.frame1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame1.setObjectName("frame1")

        self.addr_label1 = QtWidgets.QLabel(self.frame1)
        self.addr_label1.setGeometry(QtCore.QRect(10, 10, 80, 30))
        self.addr_label1.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";\n"
                                       "border: 0px solid black;")
        self.addr_label1.setObjectName("addr_label1")

        self.addr = QtWidgets.QLabel(self.frame1)
        self.addr.setGeometry(QtCore.QRect(90, 10, 620, 30))
        self.addr.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";\n"
                                "border: 0px solid black;")
        self.addr.setText("")
        self.addr.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.addr.setObjectName("addr")

        self.balance_label = QtWidgets.QLabel(self.frame1)
        self.balance_label.setGeometry(QtCore.QRect(10, 40, 80, 30))
        self.balance_label.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";\n"
                                         "border: 0px solid black;")
        self.balance_label.setObjectName("balance_label")

        self.balance = QtWidgets.QLabel(self.frame1)
        self.balance.setGeometry(QtCore.QRect(90, 40, 620, 30))
        self.balance.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";\n"
                                   "border: 0px solid black;")
        self.balance.setText("")
        self.balance.setObjectName("balance")

        self.pending_label = QtWidgets.QLabel(self.frame1)
        self.pending_label.setGeometry(QtCore.QRect(10, 70, 120, 30))
        self.pending_label.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";\n"
                                         "border: 0px solid black;")
        self.pending_label.setObjectName("pending_label")

        self.pending = QtWidgets.QLabel(self.frame1)
        self.pending.setGeometry(QtCore.QRect(90, 70, 580, 30))
        self.pending.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";\n"
                                   "border: 0px solid black;")
        self.pending.setText("")
        self.pending.setObjectName("pending")

        # Second frame title
        self.frame2_title = QtWidgets.QLabel(self.centralwidget)
        self.frame2_title.setGeometry(QtCore.QRect(14, 168, 81, 30))
        self.frame2_title.setStyleSheet("font: 75 12pt \"MS Shell Dlg 2\";")
        self.frame2_title.setObjectName("frame2_title")

        # Frame for transacting
        self.frame2 = QtWidgets.QFrame(self.centralwidget)
        self.frame2.setGeometry(QtCore.QRect(10, 200, 720, 222))
        self.frame2.setStyleSheet("border: 2px solid rgb(208, 83, 64)")
        self.frame2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame2.setObjectName("frame2")

        self.addr_label2 = QtWidgets.QLabel(self.frame2)
        self.addr_label2.setGeometry(QtCore.QRect(10, 10, 81, 30))
        self.addr_label2.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";\n"
                                       "border: 0px solid black;")
        self.addr_label2.setObjectName("addr_label2")

        self.addrInput1 = QtWidgets.QLineEdit(self.frame2)
        self.addrInput1.setGeometry(QtCore.QRect(10, 40, 632, 30))
        self.addrInput1.setObjectName("addrInput1")
        self.addrInput1.setMaxLength(34)
        self.addrInput1.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";\n"
                                      "border: 1px solid black;")

        self.addr_label3 = QtWidgets.QLabel(self.frame2)
        self.addr_label3.setGeometry(QtCore.QRect(10, 75, 162, 30))
        self.addr_label3.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";\n"
                                       "border: 0px solid black;")
        self.addr_label3.setObjectName("addr_label3")

        self.addrInput2 = QtWidgets.QLineEdit(self.frame2)
        self.addrInput2.setGeometry(QtCore.QRect(10, 106, 632, 30))
        self.addrInput2.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";\n"
                                      "border: 1px solid black;")
        self.addrInput2.setMaxLength(34)
        self.addrInput2.setObjectName("addrInput2")

        self.amount_label = QtWidgets.QLabel(self.frame2)
        self.amount_label.setGeometry(QtCore.QRect(10, 140, 156, 30))
        self.amount_label.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";\n"
                                        "border: 0px solid black;")
        self.amount_label.setObjectName("amount_label")

        self.amountInput = QtWidgets.QLineEdit(self.frame2)
        self.amountInput.setGeometry(QtCore.QRect(10, 171, 278, 30))
        self.amountInput.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";\n"
                                       "border: 1px solid black;")
        self.amountInput.setObjectName("amountInput")

        self.transactButton = QtWidgets.QPushButton(self.frame2)
        self.transactButton.setGeometry(QtCore.QRect(549, 171, 93, 30))
        self.transactButton.setObjectName("transactButton")
        self.transactButton.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";\n"
                                          "border: 1px solid black;")
        self.transactButton.clicked.connect(self.transact)

        # Third frame title
        self.frame3_title = QtWidgets.QLabel(self.centralwidget)
        self.frame3_title.setGeometry(QtCore.QRect(771, 10, 61, 31))
        self.frame3_title.setStyleSheet("font: 75 12pt \"MS Shell Dlg 2\";")
        self.frame3_title.setObjectName("frame3_title")

        # Frame for mining and block information
        self.frame3 = QtWidgets.QFrame(self.centralwidget)
        self.frame3.setGeometry(QtCore.QRect(767, 43, 720, 110))
        self.frame3.setStyleSheet("border: 2px solid rgb(208, 83, 64);")
        self.frame3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame3.setObjectName("frame3")

        self.blockNbr_label = QtWidgets.QLabel(self.frame3)
        self.blockNbr_label.setGeometry(QtCore.QRect(10, 10, 135, 30))
        self.blockNbr_label.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";\n"
                                          "border: 0px solid black;")
        self.blockNbr_label.setObjectName("blockNbr_label")

        self.blockNbr = QtWidgets.QLabel(self.frame3)
        self.blockNbr.setGeometry(QtCore.QRect(142, 10, 241, 30))
        self.blockNbr.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";\n"
                                    "border: 0px solid black;")
        self.blockNbr.setText("")
        self.blockNbr.setObjectName("blockNbr")

        self.reward_label = QtWidgets.QLabel(self.frame3)
        self.reward_label.setGeometry(QtCore.QRect(10, 40, 135, 30))
        self.reward_label.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";\n"
                                        "border: 0px solid black;")
        self.reward_label.setObjectName("reward_label")

        self.reward = QtWidgets.QLabel(self.frame3)
        self.reward.setGeometry(QtCore.QRect(88, 40, 250, 30))
        self.reward.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";\n"
                                  "border: 0px solid black;")
        self.reward.setText("")
        self.reward.setObjectName("reward")

        self.mineButton = QtWidgets.QPushButton(self.frame3)
        self.mineButton.setGeometry(QtCore.QRect(596, 70, 93, 30))
        self.mineButton.setObjectName("mineButton")
        self.mineButton.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";\n"
                                      "border: 1px solid black;")
        self.mineButton.clicked.connect(self.switch)

        # Fourth frame title
        self.frame4_title = QtWidgets.QLabel(self.centralwidget)
        self.frame4_title.setGeometry(QtCore.QRect(771, 168, 205, 31))
        self.frame4_title.setStyleSheet("font: 75 12pt \"MS Shell Dlg 2\";")
        self.frame4_title.setObjectName("frame4_title")

        # Scroll Label for Activity and Message log
        self.label = ScrollLabel(self.centralwidget)
        self.label.setGeometry(767, 200, 720, 100)
        self.label.setStyleSheet("border: 2px solid rgb(208, 83, 64)")

        # Search Label
        self.search_label = QtWidgets.QLabel(self.centralwidget)
        self.search_label.setGeometry(QtCore.QRect(771, 314, 300, 30))
        self.search_label.setStyleSheet("font: 75 12pt \"MS Shell Dlg 2\";")
        self.search_label.setObjectName("search_label")

        self.searchInput = QtWidgets.QLineEdit(self.centralwidget)
        self.searchInput.setGeometry(QtCore.QRect(771, 344, 617, 30))
        self.searchInput.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";\n"
                                       "border: 1px solid black;")
        self.searchInput.setObjectName("searchInput")

        self.searchButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchButton.setGeometry(QtCore.QRect(1397, 344, 93, 30))
        self.searchButton.setObjectName("searchButton")
        self.searchButton.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";\n"
                                        "border: 1px solid black;")
        self.searchButton.clicked.connect(self.search)

        self.minimizeButton = QtWidgets.QPushButton(self.centralwidget)
        self.minimizeButton.setGeometry(QtCore.QRect(1050, 380, 40, 40))
        self.minimizeButton.setObjectName("minimizeButton")
        self.minimizeButton.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.minimizeButton.setIcon(QIcon('static/minimizeIcon.png'))
        self.minimizeButton.clicked.connect(self.minimize)

        self.refreshButton = QtWidgets.QPushButton(self.centralwidget)
        self.refreshButton.setGeometry(QtCore.QRect(1120, 380, 40, 40))
        self.refreshButton.setObjectName("refreshButton")
        self.refreshButton.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.refreshButton.setIcon(QIcon('static/refreshIcon.png'))
        self.refreshButton.clicked.connect(self.refresh)

        self.offButton = QtWidgets.QPushButton(self.centralwidget)
        self.offButton.setGeometry(QtCore.QRect(1190, 380, 40, 40))
        self.offButton.setObjectName("offButton")
        self.offButton.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.offButton.setIcon(QIcon('static/offIcon.png'))
        self.offButton.clicked.connect(self.close)

        HomeWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(HomeWindow)
        QtCore.QMetaObject.connectSlotsByName(HomeWindow)

    def retranslateUi(self, HomeWindow):
        _translate = QtCore.QCoreApplication.translate
        HomeWindow.setWindowTitle(_translate("HomeWindow", "MainWindow"))
        self.frame1_title.setText(_translate("HomeWindow", "Wallet"))
        self.addr_label1.setText(_translate("HomeWindow", "Address:"))
        self.balance_label.setText(_translate("HomeWindow", "Balance:"))
        self.pending_label.setText(_translate("HomeWindow", "Pending:"))
        self.addr_label2.setText(_translate("HomeWindow", "Address"))
        self.amount_label.setText(_translate("HomeWindow", "Amount"))
        self.addr_label3.setText(_translate("HomeWindow", "Re-enter Address"))
        self.transactButton.setText(_translate("HomeWindow", "Transact"))
        self.frame2_title.setText(_translate("HomeWindow", "Transact"))
        self.blockNbr_label.setText(_translate("HomeWindow", "Block Number:"))
        self.reward_label.setText(_translate("HomeWindow", "Reward:"))
        self.mineButton.setText(_translate("HomeWindow", "Request"))
        self.searchButton.setText(_translate("HomeWindow", "Search"))
        self.frame3_title.setText(_translate("HomeWindow", "Mining"))
        self.frame4_title.setText(_translate("HomeWindow", "Activity & Message Log"))
        self.search_label.setText(_translate("HomeWindow", "Search For Blocks or Transactions"))
        self.initVar()
        self.client.start()

    # Function that initials the node's address, balance, pending coins
    def initVar(self):
        pendingAmount = self.client.wallet.getPendingAmount(self.client.wallet.address)
        self.addr.setText(self.client.wallet.address)
        self.balance.setText(str(self.client.wallet.amount) + " ISS COINS")
        self.pending.setText(str(pendingAmount[0]) + " ISS COINS " + "(IN: {} , OUT :{})".format(pendingAmount[1],
                                                                                                 pendingAmount[0] -
                                                                                                 pendingAmount[1]))

    def transact(self):
        sender = self.addr.text()
        receiver1 = self.addrInput1.text()
        receiver2 = self.addrInput2.text()
        amount = self.amountInput.text()
        # Checking of the address typed in both boxes are similar and that the sender has enough funds
        if receiver1 == receiver2 and self.client.transact(sender, receiver1, amount) is not None:
            self.label.setText("- Transaction Issued. " + str(self.date()))
            self.addrInput1.clear()
            self.addrInput2.clear()
            self.amountInput.clear()
            self.refresh()
        else:
            self.label.setText("- Error while generating Transaction: \n"
                               "  No Enough Funds OR Address Mismatch " + str(self.date()))

    # Function that determines whether the call to action is mining or requesting a block
    def switch(self):
        if self.mineButton.text() == "Mine":
            self.mine()
        else:
            self.request()

    # Function that requests then display the block's info
    def request(self):
        self.label.setText("- Next Block Info Request. " + str(self.date()))
        block = self.client.blockInfo()
        if block == 0:
            self.label.setText("- No Blocks Available. " + str(self.date()))
        else:
            self.blockNbr.setText(str(block.id))
            self.reward.setText(str(block.reward) + " ISS COINS")
            self.mineButton.setText("Mine")
            self.block = block

    # Function that triggers the mining process then displays when it's done
    def mine(self):
        self.client.mine(self.block)
        self.mineButton.setText("Request")
        self.blockNbr.setText("")
        self.reward.setText("")
        self.label.setText(
            "- You have succesfully calculated the block {} hash, now we will send the result to the server to check it. "
            .format(str(self.block.id)) + str(self.date()))
        self.refresh()

    # Function that refreshes all displayed values
    def refresh(self):
        self.balance.setText(str(self.client.wallet.balance()) + " ISS COINS")
        pendingAmount = self.client.wallet.getPendingAmount(self.client.wallet.address)
        self.pending.setText(str(pendingAmount[0]) + " ISS COINS " + "(IN: {} , OUT :{})".format(pendingAmount[1],
                                                                                                 pendingAmount[0] -
                                                                                                 pendingAmount[1]))

    # Function that minimizes the window
    @staticmethod
    def minimize():
        HomeWindow.showMinimized()

    # Function that closes the window
    def close(self):
        self.client.close()
        HomeWindow.close()

    # Function that gets the date in the format of h:m:s
    def date(self):
        now = datetime.datetime.now()
        res = str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
        return res

    # Function that searches for the motif that was inputted
    def search(self):
        res = self.client.database.search(self.searchInput.text())
        if res is None:
            self.label.setText("- No Object found with the search parameter")
        else:
            self.openResWindow(res)

    # Function that displays the resulting data from our search
    def openResWindow(self, res):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_ResWindow()
        self.ui.setupUi(self.window, res)
        self.window.show()


class Ui_ResWindow(object):
    def setupUi(self, ResWindow, res):
        ResWindow.setObjectName("ResWindow")
        ResWindow.setMinimumSize(QtCore.QSize(1100, 380))
        ResWindow.setMaximumSize(QtCore.QSize(1100, 380))
        ResWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(ResWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setGeometry(QtCore.QRect(10, 10, 1000, 30))
        self.titleLabel.setStyleSheet("font: 16pt \"MS Shell Dlg 2\";\n"
                                      "color: rgb(208, 83, 64);")
        self.titleLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.titleLabel.setObjectName("titleLabel")

        self.resLabel = QtWidgets.QLabel(self.centralwidget)
        self.resLabel.setGeometry(QtCore.QRect(10, 50, 1180, 490))
        self.resLabel.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.resLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.resLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.resLabel.setObjectName("label")

        ResWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(ResWindow)
        self.statusbar.setObjectName("statusbar")
        ResWindow.setStatusBar(self.statusbar)

        self.res = res

        self.retranslateUi(ResWindow)
        QtCore.QMetaObject.connectSlotsByName(ResWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("ResWindow", "Search Result Window"))
        if self.res.objectDesc.databaseTableName == "Blocks":
            self.blockRes()
        else:
            self.txRes()

    # Function that displays the resulting block
    def blockRes(self):
        self.titleLabel.setText("Search Result in Blocks :")
        self.res.objectDesc.databaseValues["transactions"] = \
            pickle.loads(self.res.objectDesc.databaseValues["transactions"])[0].transactionId
        self.resLabel.setText(json.dumps(self.res.objectDesc.databaseValues, indent=1))

    # Function that displays the resulting tx
    def txRes(self):
        self.titleLabel.setText("Search Result in Confirmed and Unconfirmed Transactions :")
        inputs = pickle.loads(self.res.objectDesc.databaseValues["inputs"])
        outputs = pickle.loads(self.res.objectDesc.databaseValues["outputs"])
        self.res.objectDesc.databaseValues["inputs"] = len(inputs)
        self.res.objectDesc.databaseValues["outputs"] = len(outputs)
        if self.res.objectDesc.databaseTableName == "Transactions":
            self.res.objectDesc.databaseValues["status"] = "Confirmed"
        else:
            self.res.objectDesc.databaseValues["status"] = "Unconfirmed"
        self.resLabel.setText(json.dumps(self.res.objectDesc.databaseValues, indent=1))


# class for scrollable label
class ScrollLabel(QScrollArea):

    # constructor
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)

        # making widget resizable
        self.setWidgetResizable(True)

        # making qwidget object
        content = QWidget(self)
        self.setWidget(content)

        # vertical box layout
        lay = QVBoxLayout(content)

        # creating label
        self.label = QLabel(content)

        # setting alignment to the text
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # making label multi-line
        self.label.setWordWrap(True)

        # adding label to the layout
        lay.addWidget(self.label)

        self.label.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        content.setStyleSheet("border: 0px solid black")

    # the setText method
    def setText(self, text):
        # setting text to the label
        txt = self.label.text()
        if txt:
            self.label.setText(txt + "\n" + text)
        else:
            self.label.setText(text)
        return True


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    HomeWindow = QtWidgets.QMainWindow()
    ui = Ui_HomeWindow()
    ui.setupUi(HomeWindow)
    HomeWindow.show()
    sys.exit(app.exec_())
