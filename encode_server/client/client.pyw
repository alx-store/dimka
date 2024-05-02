import sys
import sys
import socket
from pathlib import Path

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

module_dir = Path(__file__).parent
sys.path.append(str(module_dir.parent))
from common.protocol import *

class CryptClientWindow(QMainWindow):

    def __init__(self, parent: QMainWindow = None) -> None:
        super().__init__(parent)

        self._adapter: ClientAdapter = None
        
        uic.loadUi(module_dir / "ui/crypt_client.ui", self)
        self.ConnectBtn.clicked.connect(self.connect)
        self.EncryptBtn.clicked.connect(self.encode)
        self.DecryptBtn.clicked.connect(self.decode)

    
    def log_info(self, text: str) -> None:
        self.LogEdit.append(f'<font color="#00FF00">{text}</font>')

    def log_error(self, text: str) -> None:
        self.LogEdit.append(f'<font color="#FF0000">{text}</font>')

    def disconnect(self):
        if self._adapter:
           self.log_info("Закрытие соединения")
           self._adapter.close()
    
    def enable_controls(self, enable: bool = True) -> None:
        pass
    
    def encode(self) -> None:
        self.process_data("encode")

    def decode(self) -> None:
        self.process_data("decode")

    def process_data(self, command: str) -> None:
        input_file = Path(self.InFileEdit.text())
        alg_name = self.AlgCombo.currentText()
        if not input_file.is_file:
            QMessageBox.critical(f"Файл {input_file} не найден")
            return

        with input_file.open("rb") as f:
            data = f.read()

        if self._adapter:
            try:
                self.log_info(f"Запрос на кодирование ({command}), алгортим: {alg_name}, размер данных {len(data)}")
                rsp = self._adapter.get(SocketRequest(command, {"alg_name": "first_alg"}, data))
                rsp.check_status()
                self.log_info(f"Сервер вернул даннйе, размер {len(rsp.payload)}")
            except Exception as e:
                self.log_error(f"Ошибка на сервере {str(e)}")
        else:
            self.log_error("Подключение к серверу не установлено")
        
        output_file = Path(self.OutFileEdit.text())
        with output_file.open("wb") as f:
            f.write(rsp.payload)

    def connect(self):
        self.disconnect()
        self.log_info(f"Соединение с {self.AddressEdit.text()}:{self.PortEdit.value()}...")
        try:
            self._adapter = ClientAdapter(socket.create_connection((self.AddressEdit.text(), self.PortEdit.value())))
            self.log_info("Соединение установлено")
            self.log_info("Запрос списка алгоритмов")
            rsp = self._adapter.get(SocketRequest("list"))
            rsp.check_status()
            self.AlgCombo.clear()
            self.AlgCombo.addItems(rsp.payload.decode().splitlines())
        except Exception as e:
            self.log_error(str(e))
            self.disconnect()





if __name__ == "__main__":
    # create application
    app = QApplication(sys.argv)
    app.setApplicationName("Демонстрация алгоритма шифрования")

    # create widget
    w = CryptClientWindow()
    w.show()

    # execute application
    app.exec_()

    sys.exit()