import sys
import os

from PyQt5.QtWidgets import QMessageBox

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

from permutation_cipher import encrypt_per, decrypt_per
from replacement_cipher import encrypt_rep, decrypt_rep


class HelpForm(QDialog):
    def __init__(self, parent: QDialog = None) -> None:
        super().__init__(parent)
        uic.loadUi("ui/helpdialog.ui", self)
        self.setWindowIcon(QIcon("ui/mainicon.png"))
        
        self.ButtonBox.buttons().clear()
        self.ButtonBox.addButton("Закрыть", QDialogButtonBox.RejectRole)

    def exec(self, filename: str):
        if os.path.exists(filename):
            self.RefBrowser.setSource(QUrl(filename))
        super().exec()


class MainForm(QMainWindow):
    main_help_file = "help/Шифры.md"
    trans_table_1 = str.maketrans("", "", ' !"№;%:?*()_+-=/|}{][@#$^&,.<>0123456789')
    trans_table_2 = str.maketrans("", "", ' !"№;%:?*()+-=/|}{][@#$^&,.<>0123456789')

    def __init__(self, parent: QMainWindow = None) -> None:
        super().__init__(parent)

        uic.loadUi("ui/main.ui", self)
        self.setWindowIcon(QIcon("ui/mainicon.png"))

        self.Alph = []
        self.Column = 0
        self.Line = 0

        if os.path.exists(self.main_help_file):
            self.HelpBrowser.setSource(QUrl(self.main_help_file))

        self.SetLangGroup: QActionGroup = QActionGroup(self)
        self.SetLangGroup.addAction(self.SetRusAction)
        self.SetLangGroup.addAction(self.SetEngAction)
        self.SetLangGroup.setExclusive(True)
        self.SetLangGroup.triggered.connect(self.lang_changed)
        self.lang_changed()

        self.SetModeGroup: QActionGroup = QActionGroup(self)
        self.SetModeGroup.addAction(self.SetEncryptAction)
        self.SetModeGroup.addAction(self.SetDecryptAction)
        self.SetModeGroup.setExclusive(True)
        self.SetModeGroup.triggered.connect(self.mode_changed)
        self.mode_changed()

        self.ChangeTextButton.clicked.connect(self.change_text)

        self.HelpEncAction.triggered.connect(self.showhelp)
        self.HelpDecAction.triggered.connect(self.showhelp)
        self.HelpToolsAction.triggered.connect(self.showhelp)


    def showhelp(self):
        help_file = {
            self.HelpEncAction: "help/HelpEncryption.md",
            self.HelpDecAction: "help/HelpDecryption.md",
            self.HelpToolsAction: "help/HelpTools.md",
        }.get(self.sender(), "")
        help_form = HelpForm()
        help_form.exec(help_file)

    def lang_changed(self) -> None:
        if self.SetLangGroup.checkedAction() == self.SetRusAction:
            self.Alph: str = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
            self.Column = 4
            self.Line = 8
        else:
            self.Alph: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            self.Column = 5
            self.Line = 5

    def mode_changed(self) -> None:
        if self.SetModeGroup.checkedAction() == self.SetEncryptAction:
            self.ActionButton.setText("Зашифровать")
            self.ActionButton.clicked.connect(self.encrypt)
            self.Result1Label.setText("Результат после \"Замены\"")
        else:
            self.ActionButton.setText("Расшифровать")
            self.ActionButton.clicked.connect(self.decrypt)
            self.Result1Label.setText("Результат после \"Перестановки\"")

    def change_text(self):
        self.InputEdit.setText(self.Result2Edit.text())
        self.Result1Edit.setText("")
        self.Result2Edit.setText("")

    @property
    def key_permutation(self) -> int:
        return self.KeySpin.value()

    @property
    def key_replacement(self) -> int:
        return self.KeyEdit.text().translate(self.trans_table_1).upper()

    def encrypt(self) -> None:
        text = self.InputEdit.text().translate(self.trans_table_1).upper()

        try:
            encrypt_rep_result = encrypt_rep(self.Alph, self.Line, self.Column, self.key_replacement, text)
            self.Result1Edit.setText(encrypt_rep_result)
            self.Result2Edit.setText(encrypt_per(self.key_permutation, encrypt_rep_result))
        except ValueError:
            QMessageBox(
                QMessageBox.Icon.Critical,
                "Ошибка выполнения",
                "Произошла ошибка, вероятно неверный ввод данных",
            ).exec()
        except ZeroDivisionError:
            QMessageBox(
                QMessageBox.Icon.Critical,
                "Ошибка выполнения",
                "Ключ не может быть равен нулю",
            ).exec()
        except Exception as e:
            QMessageBox(
                QMessageBox.Icon.Critical,
                "Ошибка выполнения",
                f"Ошибка выполнения программы: {str(e)}",
            ).exec()

    def decrypt(self) -> None:
        cipher = self.InputEdit.text().translate(self.trans_table_2).upper()
        try:
            decrypt_per_result = decrypt_per(cipher, self.key_permutation, self.Alph)
            self.Result1Edit.setText(decrypt_per_result)
            self.Result2Edit.setText(decrypt_rep(self.Alph, self.Line, self.Column, self.key_replacement, decrypt_per_result.replace("_", "")))
        except ValueError:
            QMessageBox(
                QMessageBox.Icon.Critical,
                "Ошибка выполнения",
                "Произошла ошибка, вероятно неверный ввод данных",
            ).exec()

        except IndexError:
            QMessageBox(
                QMessageBox.Icon.Critical,
                "Ошибка выполнения",
                "Произошла ошибка, длина шифра должна быть кратна 4",
            ).exec()

        except ZeroDivisionError:
            QMessageBox(
                QMessageBox.Icon.Critical,
                "Ошибка выполнения",
                "Ключ не может быть равен нулю",
            ).exec()
        except Exception as e:
            QMessageBox(
                QMessageBox.Icon.Critical,
                "Ошибка выполнения",
                f"Ошибка выполнения программы: {str(e)}",
            ).exec()


if __name__ == "__main__":
    # create application
    app = QApplication(sys.argv)
    app.setApplicationName("Демонстрация алгоритма шифрования")

    # create widget
    w = MainForm()
    w.show()

    # execute application
    app.exec_()

    sys.exit()
