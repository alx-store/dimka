# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Alex\YandexDisk\projects\py\misc\edu\crypt\ui\main.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(908, 594)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.HelpBrowser = QtWidgets.QTextBrowser(self.frame)
        self.HelpBrowser.setObjectName("HelpBrowser")
        self.verticalLayout_2.addWidget(self.HelpBrowser)
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.Result1Label = QtWidgets.QLabel(self.frame_2)
        self.Result1Label.setObjectName("Result1Label")
        self.gridLayout_2.addWidget(self.Result1Label, 2, 0, 1, 2)
        self.KeySpin = QtWidgets.QSpinBox(self.frame_2)
        self.KeySpin.setEnabled(True)
        self.KeySpin.setObjectName("KeySpin")
        self.gridLayout_2.addWidget(self.KeySpin, 1, 2, 1, 1)
        self.InputLabel = QtWidgets.QLabel(self.frame_2)
        self.InputLabel.setObjectName("InputLabel")
        self.gridLayout_2.addWidget(self.InputLabel, 0, 0, 1, 1)
        self.Result2Label = QtWidgets.QLabel(self.frame_2)
        self.Result2Label.setObjectName("Result2Label")
        self.gridLayout_2.addWidget(self.Result2Label, 4, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 2, 1, 1)
        self.ActionButton = QtWidgets.QPushButton(self.frame_2)
        self.ActionButton.setObjectName("ActionButton")
        self.gridLayout_2.addWidget(self.ActionButton, 1, 3, 1, 1)
        self.InputEdit = QtWidgets.QLineEdit(self.frame_2)
        self.InputEdit.setObjectName("InputEdit")
        self.gridLayout_2.addWidget(self.InputEdit, 1, 0, 1, 1)
        self.KeyEdit = QtWidgets.QLineEdit(self.frame_2)
        self.KeyEdit.setObjectName("KeyEdit")
        self.gridLayout_2.addWidget(self.KeyEdit, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 1, 1, 1)
        self.Result1Edit = QtWidgets.QLineEdit(self.frame_2)
        self.Result1Edit.setReadOnly(True)
        self.Result1Edit.setObjectName("Result1Edit")
        self.gridLayout_2.addWidget(self.Result1Edit, 3, 0, 1, 3)
        self.Result2Edit = QtWidgets.QLineEdit(self.frame_2)
        self.Result2Edit.setEnabled(True)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Result2Edit.setFont(font)
        self.Result2Edit.setReadOnly(False)
        self.Result2Edit.setObjectName("Result2Edit")
        self.gridLayout_2.addWidget(self.Result2Edit, 5, 0, 1, 3)
        self.ChangeTextButton = QtWidgets.QPushButton(self.frame_2)
        self.ChangeTextButton.setObjectName("ChangeTextButton")
        self.gridLayout_2.addWidget(self.ChangeTextButton, 3, 3, 3, 1)
        self.verticalLayout.addWidget(self.frame_2, 0, QtCore.Qt.AlignBottom)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 908, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.LangMenu = QtWidgets.QMenu(self.menu)
        self.LangMenu.setObjectName("LangMenu")
        self.ModeMenu = QtWidgets.QMenu(self.menu)
        self.ModeMenu.setObjectName("ModeMenu")
        self.Reference = QtWidgets.QMenu(self.menubar)
        self.Reference.setObjectName("Reference")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.SetRusAction = QtWidgets.QAction(MainWindow)
        self.SetRusAction.setCheckable(True)
        self.SetRusAction.setChecked(True)
        self.SetRusAction.setObjectName("SetRusAction")
        self.SetEngAction = QtWidgets.QAction(MainWindow)
        self.SetEngAction.setCheckable(True)
        self.SetEngAction.setObjectName("SetEngAction")
        self.SetEncryptAction = QtWidgets.QAction(MainWindow)
        self.SetEncryptAction.setCheckable(True)
        self.SetEncryptAction.setChecked(True)
        self.SetEncryptAction.setObjectName("SetEncryptAction")
        self.SetDecryptAction = QtWidgets.QAction(MainWindow)
        self.SetDecryptAction.setCheckable(True)
        self.SetDecryptAction.setObjectName("SetDecryptAction")
        self.ExitAction = QtWidgets.QAction(MainWindow)
        self.ExitAction.setObjectName("ExitAction")
        self.HelpEncAction = QtWidgets.QAction(MainWindow)
        self.HelpEncAction.setObjectName("HelpEncAction")
        self.HelpDecAction = QtWidgets.QAction(MainWindow)
        self.HelpDecAction.setObjectName("HelpDecAction")
        self.HelpToolsAction = QtWidgets.QAction(MainWindow)
        self.HelpToolsAction.setObjectName("HelpToolsAction")
        self.LangMenu.addAction(self.SetRusAction)
        self.LangMenu.addAction(self.SetEngAction)
        self.ModeMenu.addAction(self.SetEncryptAction)
        self.ModeMenu.addAction(self.SetDecryptAction)
        self.menu.addAction(self.LangMenu.menuAction())
        self.menu.addAction(self.ModeMenu.menuAction())
        self.menu.addSeparator()
        self.menu.addAction(self.ExitAction)
        self.Reference.addAction(self.HelpEncAction)
        self.Reference.addAction(self.HelpDecAction)
        self.Reference.addAction(self.HelpToolsAction)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.Reference.menuAction())

        self.retranslateUi(MainWindow)
        self.ExitAction.triggered.connect(MainWindow.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Демонстрация алгоритма шифрования"))
        self.Result1Label.setText(_translate("MainWindow", "Результат после \"Замены\""))
        self.InputLabel.setText(_translate("MainWindow", "Текст"))
        self.Result2Label.setText(_translate("MainWindow", "Конечный результат"))
        self.label_3.setText(_translate("MainWindow", "Ключ перестановки"))
        self.ActionButton.setText(_translate("MainWindow", "Старт"))
        self.label_2.setText(_translate("MainWindow", "Ключ замены"))
        self.ChangeTextButton.setText(_translate("MainWindow", "Подставить"))
        self.menu.setTitle(_translate("MainWindow", "Настройки"))
        self.LangMenu.setTitle(_translate("MainWindow", "Язык ввода"))
        self.ModeMenu.setTitle(_translate("MainWindow", "Режим"))
        self.Reference.setTitle(_translate("MainWindow", "Справка"))
        self.SetRusAction.setText(_translate("MainWindow", "Русский"))
        self.SetEngAction.setText(_translate("MainWindow", "Английский"))
        self.SetEncryptAction.setText(_translate("MainWindow", "Зашифровать"))
        self.SetDecryptAction.setText(_translate("MainWindow", "Расшифровать"))
        self.ExitAction.setText(_translate("MainWindow", "Выход"))
        self.HelpEncAction.setText(_translate("MainWindow", "Шифрование"))
        self.HelpDecAction.setText(_translate("MainWindow", "Расшифрование"))
        self.HelpToolsAction.setText(_translate("MainWindow", "Инструменты"))
