import sys
import sys
import socket
import math
from pathlib import Path
from threading import Thread, Lock, current_thread

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

module_dir = Path(__file__).parent
sys.path.append(str(module_dir.parent))
from common.protocol import *


class ClientWorker(Thread):
    """Клиентский поток, отправляющий часть данных на сервер и получающий кодированный ответ
    """
    def __init__(self, adapter: ClientAdapter, command: str, alg_name: str) -> None:
        super().__init__()
        # Адаптер с соединением к сокету (создается клиентским приложением)
        self.adapter: ClientAdapter = adapter
        self.command: str = command
        self.alg_name: str = alg_name
        self.data: bytes = None
        # Callback-функция для записи в лог
        self.logger = None
        # Здесь будем хранить ответ сервера
        self.response: SocketResponse = None

    def log(self, message: str, is_error: bool = False) -> None:
        """Запись в лог

        Args:
            message (str): сообщение
            is_error (bool, optional): признак сообщения об ошибке (будет выводиться красным)
        """
        if self.logger:
            self.logger(f"Поток {self.name}: {message}", is_error)

    def run(self) -> None:
        """Основные действия по работе с сервером
        """
        if self.adapter:
            try:
                self.log(f"запрос на кодирование ({self.command}), алгоритм: {self.alg_name}, размер данных {len(self.data)}")
                self.response = self.adapter.get(SocketRequest(self.command, {"alg_name": self.alg_name}, self.data))
                self.response.check_status()
                self.log(f"сервер вернул данные, размер {len(self.response.payload)}")
            except Exception as e:
                self.log(f"ошибка на сервере {str(e)}", is_error=True)
        else:
            self.log("подключение к серверу не установлено", is_error=True)

class CryptClientWindow(QMainWindow):
    """Главное окно приложения
    """
    def __init__(self, parent: QMainWindow = None) -> None:
        super().__init__(parent)

        self._adapter: ClientAdapter = None
        
        uic.loadUi(module_dir / "ui/client.ui", self)
        self.setWindowTitle("Демонстрация алгоритма шифрования")
        self.ConnectBtn.clicked.connect(self.connect)
        self.EncryptBtn.clicked.connect(lambda : self.process_data("encode"))
        self.DecryptBtn.clicked.connect(lambda : self.process_data("decode"))
        self.InFileBtn.clicked.connect(lambda : self.select_file(is_input=True))
        self.OutFileBtn.clicked.connect(lambda : self.select_file(is_input=False))

        self.info_lock: Lock = Lock()
        self.in_process: bool = False

        self.enable_controls()

    def enable_controls(self) -> None:
        """Переключение доступности элементов управления в зависимости от того запущен ли процесс кодирования, установлено ли соединение и указаны ли все данные
        """
        self.AddressEdit.setEnabled(not self.in_process)
        self.PortEdit.setEnabled(not self.in_process)
        self.InFileEdit.setEnabled(not self.in_process)
        self.OutFileEdit.setEnabled(not self.in_process)
        self.AlgCombo.setEnabled(not self.in_process)
        self.PartCountEdit.setEnabled(not self.in_process)

        self.InFileBtn.setEnabled(not self.in_process)
        self.OutFileBtn.setEnabled(not self.in_process)
        self.ConnectBtn.setEnabled(not self.in_process)

        files_selected = (self.InFileEdit.text() != "") and (self.OutFileEdit.text() != "") 
        self.EncryptBtn.setEnabled(not self.in_process and files_selected and (self._adapter != None))
        self.DecryptBtn.setEnabled(not self.in_process and files_selected and (self._adapter != None))
   
    def log_info(self, text: str, is_error: bool = False) -> None:
        """Вывод в лог

        Args:
            message (str): сообщение
            is_error (bool, optional): признак сообщения об ошибке (будет выводиться красным)
        """
        # Устанавливаем блокировку - несколько потоков могут одновременно пытаться что-то записать
        self.info_lock.acquire()
        try:
            color = "#FF0000" if is_error else "#00FF00"
            self.LogEdit.append(f'<font color="{color}">{text}</font>')
            app.processEvents()
        finally:
            # Не забыть освободить блокировку
            self.info_lock.release()

    def select_file(self, is_input: bool = True) -> None:
        """Выбор файла

        Args:
            is_input (bool, optional): признак - входной или выходной файл
        """
        # Если выбираем входной файл, то поднимаем диалог открытия файла и записываем в поле ввода входного файла
        # Если выбираем вЫходной файл, то поднимаем диалог сохранения файла и записываем в поле ввода вЫходного файла
        file_dialog = QFileDialog(self) 
        file_dialog.setAcceptMode(QFileDialog.AcceptOpen if is_input else QFileDialog.AcceptSave)
        file_dialog.setFileMode(QFileDialog.ExistingFile if is_input else QFileDialog.AnyFile)
        edit_control: QTextEdit = None
        if is_input:
            f = file_dialog.getOpenFileName()
            edit_control = self.InFileEdit
        else:
            f = file_dialog.getSaveFileName()
            edit_control = self.OutFileEdit
        if f[0]:
            edit_control.setText(f[0])
        # Обновить состояние элементов управления
        self.enable_controls()
    
    def disconnect(self):
        """Завершение соединения с сервером
        """
        if self._adapter:
           self.log_info("Закрытие соединения")
           self._adapter.close()
        self.enable_controls()
      
    def _set_in_process(self, in_process: bool) -> None:
        self.in_process = in_process
        self.enable_controls()

    def process_data(self, command: str) -> None:
        """Кодирование и декодирование файлы

        Args:
            command (str): команда: encode - для кодирования, decode - для декодирования
        """
        # Имя файла и название алгоритма
        input_file = Path(self.InFileEdit.text())
        alg_name = self.AlgCombo.currentText()
        if not input_file.is_file:
            QMessageBox.critical(f"Файл {input_file} не найден")
            return
        try:
            # Помечаем, что процесс начат - контролы не доступны
            self._set_in_process(True)
            # Проверить алгоритм на корректность
            self._adapter.get(SocketRequest("check_alg")).check_status()

            # Размер файла, количество частей и размер части
            file_sise = input_file.stat().st_size
            part_count = self.PartCountEdit.value()
            part_size = math.ceil(file_sise / part_count)

            # Здесь будет список потоков, обрабатывающих данные
            worker_list = []
        
            with input_file.open("rb") as f:
                # Считываем файл порциями - по количеству потоков
                for i in range(part_count):
                    # Для каждой порции - свой поток. Для потока - адаптер и сокет
                    adapter = ClientAdapter(socket.create_connection((self.AddressEdit.text(), self.PortEdit.value())))
                    worker = ClientWorker(adapter, command, alg_name)
                    worker.name = str(i)
                    # передача данных в поток
                    worker.data = f.read(part_size)
                    # передаем ссылку на функцию логгирования в поток
                    worker.logger = self.log_info
                    # поток добавляем в список и запускаем
                    worker_list.append(worker)
                    worker.start()
                    self.log_info(f"Запущен поток {worker.name}, передано {len(worker.data)} байт")
            # Ждем когда все потоки завершатся
            for worker in worker_list:
                worker.join()

            # Выгружаем данные из списка потоков последовательно - от первого потока до последнего
            output_file = Path(self.OutFileEdit.text())
            with output_file.open("wb") as f:
                for worker in worker_list:
                    # Если ответ сервера не получен или неуспешен - выбрасываем исключение
                    if worker.response and worker.response.code == SERVER_OK:
                        f.write(worker.response.payload)
                    else:
                        QMessageBox.critical(self, "Ошибка", "Ошибка кодирования данных.\nСм. протокол работы приложения")
                        return
            QMessageBox.information(self, "Кодирование данных", "Кодирование данных завершено успешно")
        finally:
            # Снимаем отметку того, что процесс запущен - контролы доступны
            self._set_in_process(False)

    def connect(self):
        """Остановка соединения с сервером
        """
        # Если уже было установлено - отсоединяемся
        self.disconnect()
        self.log_info(f"Соединение с {self.AddressEdit.text()}:{self.PortEdit.value()}...")
        try:
            # Создаем новые сокет и адаптер
            self._adapter = ClientAdapter(socket.create_connection((self.AddressEdit.text(), self.PortEdit.value())))
            self.log_info("Соединение установлено")
            self.log_info("Запрос списка алгоритмов")
            # Запрос списка алгоритмов
            rsp = self._adapter.get(SocketRequest("list"))
            rsp.check_status()
            self.AlgCombo.clear()
            self.AlgCombo.addItems(rsp.payload.decode().splitlines())
        except Exception as e:
            self.log_info(str(e), is_error=True)
            # Отсоединяемся в случае ошибки
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