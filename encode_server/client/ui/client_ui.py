# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Alex\YandexDisk\projects\py\dimka\encode_server\client\ui\client.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CryptClientWindow(object):
    def setupUi(self, CryptClientWindow):
        CryptClientWindow.setObjectName("CryptClientWindow")
        CryptClientWindow.resize(609, 441)
        self.centralwidget = QtWidgets.QWidget(CryptClientWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.ControlFrame = QtWidgets.QFrame(self.splitter)
        self.ControlFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ControlFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ControlFrame.setObjectName("ControlFrame")
        self.gridLayout = QtWidgets.QGridLayout(self.ControlFrame)
        self.gridLayout.setObjectName("gridLayout")
        self.AddressLabel = QtWidgets.QLabel(self.ControlFrame)
        self.AddressLabel.setObjectName("AddressLabel")
        self.gridLayout.addWidget(self.AddressLabel, 0, 0, 1, 1)
        self.ConnectBtn = QtWidgets.QPushButton(self.ControlFrame)
        self.ConnectBtn.setObjectName("ConnectBtn")
        self.gridLayout.addWidget(self.ConnectBtn, 1, 4, 1, 2)
        self.AddressEdit = QtWidgets.QLineEdit(self.ControlFrame)
        self.AddressEdit.setObjectName("AddressEdit")
        self.gridLayout.addWidget(self.AddressEdit, 0, 1, 1, 3)
        self.PortEdit = QtWidgets.QSpinBox(self.ControlFrame)
        self.PortEdit.setMaximum(100000)
        self.PortEdit.setProperty("value", 10001)
        self.PortEdit.setObjectName("PortEdit")
        self.gridLayout.addWidget(self.PortEdit, 0, 4, 1, 2)
        self.InFileBtn = QtWidgets.QToolButton(self.ControlFrame)
        self.InFileBtn.setObjectName("InFileBtn")
        self.gridLayout.addWidget(self.InFileBtn, 3, 5, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 6, 0, 1, 3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 3)
        self.InFileLabel = QtWidgets.QLabel(self.ControlFrame)
        self.InFileLabel.setObjectName("InFileLabel")
        self.gridLayout.addWidget(self.InFileLabel, 3, 0, 1, 1)
        self.AlgLabel = QtWidgets.QLabel(self.ControlFrame)
        self.AlgLabel.setObjectName("AlgLabel")
        self.gridLayout.addWidget(self.AlgLabel, 2, 0, 1, 1)
        self.AlgCombo = QtWidgets.QComboBox(self.ControlFrame)
        self.AlgCombo.setObjectName("AlgCombo")
        self.gridLayout.addWidget(self.AlgCombo, 2, 1, 1, 5)
        self.OutFileLabel = QtWidgets.QLabel(self.ControlFrame)
        self.OutFileLabel.setObjectName("OutFileLabel")
        self.gridLayout.addWidget(self.OutFileLabel, 4, 0, 1, 1)
        self.InFileEdit = QtWidgets.QLineEdit(self.ControlFrame)
        self.InFileEdit.setObjectName("InFileEdit")
        self.gridLayout.addWidget(self.InFileEdit, 3, 1, 1, 4)
        self.OutFileBtn = QtWidgets.QToolButton(self.ControlFrame)
        self.OutFileBtn.setObjectName("OutFileBtn")
        self.gridLayout.addWidget(self.OutFileBtn, 4, 5, 1, 1)
        self.ThreadCountLabel = QtWidgets.QLabel(self.ControlFrame)
        self.ThreadCountLabel.setObjectName("ThreadCountLabel")
        self.gridLayout.addWidget(self.ThreadCountLabel, 5, 0, 1, 1)
        self.PartCountEdit = QtWidgets.QSpinBox(self.ControlFrame)
        self.PartCountEdit.setMinimum(1)
        self.PartCountEdit.setProperty("value", 5)
        self.PartCountEdit.setObjectName("PartCountEdit")
        self.gridLayout.addWidget(self.PartCountEdit, 5, 1, 1, 1)
        self.OutFileEdit = QtWidgets.QLineEdit(self.ControlFrame)
        self.OutFileEdit.setObjectName("OutFileEdit")
        self.gridLayout.addWidget(self.OutFileEdit, 4, 1, 1, 4)
        self.EncryptBtn = QtWidgets.QPushButton(self.ControlFrame)
        self.EncryptBtn.setObjectName("EncryptBtn")
        self.gridLayout.addWidget(self.EncryptBtn, 6, 3, 1, 1)
        self.DecryptBtn = QtWidgets.QPushButton(self.ControlFrame)
        self.DecryptBtn.setObjectName("DecryptBtn")
        self.gridLayout.addWidget(self.DecryptBtn, 6, 4, 1, 2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 7, 3, 1, 1)
        self.LogEdit = QtWidgets.QTextEdit(self.splitter)
        self.LogEdit.setObjectName("LogEdit")
        self.gridLayout_2.addWidget(self.splitter, 0, 0, 1, 1)
        CryptClientWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(CryptClientWindow)
        self.statusbar.setObjectName("statusbar")
        CryptClientWindow.setStatusBar(self.statusbar)

        self.retranslateUi(CryptClientWindow)
        QtCore.QMetaObject.connectSlotsByName(CryptClientWindow)

    def retranslateUi(self, CryptClientWindow):
        _translate = QtCore.QCoreApplication.translate
        CryptClientWindow.setWindowTitle(_translate("CryptClientWindow", "MainWindow"))
        self.AddressLabel.setText(_translate("CryptClientWindow", "Адрес сервиса"))
        self.ConnectBtn.setText(_translate("CryptClientWindow", "Соединиться"))
        self.AddressEdit.setText(_translate("CryptClientWindow", "127.0.0.1"))
        self.InFileBtn.setText(_translate("CryptClientWindow", "..."))
        self.InFileLabel.setText(_translate("CryptClientWindow", "Входной файл"))
        self.AlgLabel.setText(_translate("CryptClientWindow", "Алгоритм"))
        self.OutFileLabel.setText(_translate("CryptClientWindow", "Выходной файл"))
        self.OutFileBtn.setText(_translate("CryptClientWindow", "..."))
        self.ThreadCountLabel.setText(_translate("CryptClientWindow", "Количество потоков"))
        self.EncryptBtn.setText(_translate("CryptClientWindow", "Зашифровать"))
        self.DecryptBtn.setText(_translate("CryptClientWindow", "Расшифровать"))
        self.LogEdit.setHtml(_translate("CryptClientWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\" bgcolor=\"#000000\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))