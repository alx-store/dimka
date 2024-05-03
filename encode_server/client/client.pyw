import sys
import sys
import socket
import math
from pathlib import Path
from threading import Thread
from typing import Mapping

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

module_dir = Path(__file__).parent
sys.path.append(str(module_dir.parent))
from common.protocol import *


class ClienWorker(Thread):
    def __init__(self, id: int, adapter: ClientAdapter, command: str, alg_name: str) -> None:
        super().__init__()
        self.id = id
        self.adapter: ClientAdapter = adapter
        self.command: str = command
        self.alg_name: str = alg_name
        self.data: bytes = None
        self.logger = None
        self.response: SocketResponse = None

    def log(self, message: str, is_error: bool = False) -> None:
        if self.logger:
            self.logger(f"Поток {self.id}: {message}", is_error)

    def run(self) -> None:
        if self.adapter:
            try:
                self.log(f"запрос на кодирование ({self.command}), алгортим: {self.alg_name}, размер данных {len(self.data)}")
                self.response = self.adapter.get(SocketRequest(self.command, {"alg_name": self.alg_name}, self.data))
                self.response.check_status()
                self.log(f"сервер вернул данные, размер {len(self.response.payload)}")
            except Exception as e:
                self.log(f"ошибка на сервере {str(e)}", is_error=True)
        else:
            self.log("подключение к серверу не установлено", is_error=True)

class CryptClientWindow(QMainWindow):

    def __init__(self, parent: QMainWindow = None) -> None:
        super().__init__(parent)

        self._adapter: ClientAdapter = None
        
        uic.loadUi(module_dir / "ui/client.ui", self)
        self.ConnectBtn.clicked.connect(self.connect)
        self.EncryptBtn.clicked.connect(self.encode)
        self.DecryptBtn.clicked.connect(self.decode)
        self.InFileBtn.clicked.connect(self.get_input_file)
        self.OutFileBtn.clicked.connect(self.get_output_file)

    
    def log_info(self, text: str, is_error: bool = False) -> None:
        color = "#FF0000" if is_error else "#00FF00"
        self.LogEdit.append(f'<font color="{color}">{text}</font>')
        app.processEvents()

    def get_input_file(self) -> None:
        file_name = self.select_file(True)
        if file_name:
            self.InFileEdit.setText(file_name)

    def get_output_file(self) -> None:
        file_name = self.select_file(False)
        if file_name:
            self.OutFileEdit.setText(file_name)

    def select_file(self, is_input: bool = True) -> None:
        file_dialog = QFileDialog(self) 
        file_dialog.setAcceptMode(QFileDialog.AcceptOpen if is_input else QFileDialog.AcceptSave)
        file_dialog.setFileMode(QFileDialog.ExistingFile if is_input else QFileDialog.AnyFile)
        if is_input:
            f = file_dialog.getOpenFileName()
        else:
            f = file_dialog.getSaveFileName()
        return f[0]
    
    def disconnect(self):
        if self._adapter:
           self.log_info("Закрытие соединения")
           self._adapter.close()
    
    
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

        file_sise = input_file.stat().st_size
        part_count = self.PartCountEdit.value()
        part_size = math.ceil(file_sise / part_count)
        worker_list = []
    
        with input_file.open("rb") as f:
            for i in range(part_count):
                adapter = ClientAdapter(socket.create_connection((self.AddressEdit.text(), self.PortEdit.value())))
                worker = ClienWorker(i, adapter, command, alg_name)
                worker.data = f.read(part_size)
                worker.logger = self.log_info
                worker_list.append(worker)
                worker.start()
                self.log_info(f"Запущен поток {i}, передано {len(worker.data)} байт")
        for worker in worker_list:
            worker.join()

        output_file = Path(self.OutFileEdit.text())
        with output_file.open("wb") as f:
            for worker in worker_list:
                if worker.response and worker.response.code == SERVER_OK:
                    f.write(worker.response.payload)
                else:
                    QMessageBox.critical(self, "Ошибка", "Ошибка кодирования данных.\nСм. протокол работы приложения")
                    return
            QMessageBox.information(self, "Кодирование данных", "Кодирование данных завершено успешно")

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