from PyQt5 import QtCore, QtGui, QtWidgets
from home import Ui_HomeWindow
import init_database


class Ui_Welcome(object):
    def setupUi(self, Welcome):
        Welcome.setObjectName("Welcome")
        Welcome.resize(1000, 500)
        Welcome.setMinimumSize(QtCore.QSize(1000, 500))
        Welcome.setMaximumSize(QtCore.QSize(1000, 500))
        Welcome.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                              "background-color: rgb(255, 255, 255);\n"
                              "border-color: rgb(0, 0, 0);")
        self.centralwidget = QtWidgets.QWidget(Welcome)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 285, 110))
        self.label.setMinimumSize(QtCore.QSize(285, 110))
        self.label.setMaximumSize(QtCore.QSize(285, 110))
        self.label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                 "")
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("static/iss.png"))
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 150, 231, 31))
        self.label_4.setObjectName("label_4")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(10, 190, 930, 101))
        self.label_8.setMaximumSize(QtCore.QSize(980, 16777215))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(10, 300, 930, 101))
        self.label_9.setMaximumSize(QtCore.QSize(980, 16777215))
        self.label_9.setObjectName("label_9")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(830, 430, 100, 30))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet("background-color: rgb(255, 0, 0);\n"
                                      "color: rgb(255, 255, 255);\n"
                                      "font: 12pt \"MS Shell Dlg 2\";")
        self.pushButton.clicked.connect(self.advance)

        Welcome.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Welcome)
        self.statusbar.setObjectName("statusbar")
        Welcome.setStatusBar(self.statusbar)

        self.retranslateUi(Welcome)
        QtCore.QMetaObject.connectSlotsByName(Welcome)

    def retranslateUi(self, Welcome):
        _translate = QtCore.QCoreApplication.translate
        Welcome.setWindowTitle(_translate("Welcome", "MainWindow"))
        self.label_4.setText(_translate("Welcome",
                                        "<html><head/><body><p><span style=\" font-size:12pt; font-style:italic;\">Welcome to Isscoin Core.</span></p></body></html>"))
        self.label_8.setText(_translate("Welcome",
                                        "<html><head/><body><p><span style=\" font-size:12pt;\">Isscoin core will store it\'s data in the current working directory. </span></p><p><span style=\" font-size:12pt;\">Isscoin core will download and store a copy of the Isscoin block chain. The wallet will also be stored in </span></p><p><span style=\" font-size:12pt;\">this directory.</span></p></body></html>"))
        self.label_9.setText(_translate("Welcome",
                                        "<html><head/><body><p><span style=\" font-size:12pt;\">When you click OK, Isscoin Core will begin to download and process the Isscoin block chain starting with </span></p><p><span style=\" font-size:12pt;\">the earliest transactions when Isscoin initally launched. Each time you run Isscoin Core, it will continue </span></p><p><span style=\" font-size:12pt;\">downloading where it left.</span></p></body></html>"))
        self.pushButton.setText(_translate("Welcome", "OK"))

    def advance(self):
        init_database.main("database.db")
        self.openHomeWindow()
        Welcome.hide()

    def openHomeWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_HomeWindow()
        self.ui.setupUi(self.window)
        self.window.show()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Welcome = QtWidgets.QMainWindow()
    ui = Ui_Welcome()
    ui.setupUi(Welcome)
    Welcome.show()
    sys.exit(app.exec_())
