import sys
import socket
import threading
import logging
import importlib
from pathlib import Path
from types import ModuleType

module_dir = Path(__file__).parent
sys.path.append(str(module_dir.parent))

from common.protocol import *

# Здесь должны лежать алгоритмы
alg_dir = module_dir / "alg"

logger = logging.getLogger("encode-server")

PORT = 10001
MAX_CONNECTIONS = 1000

class Worker(threading.Thread):
    """Поток обработки клиентского соединия
    Args:
        threading (_type_): _description_
    """
    def __init__(self, socket: socket.socket, address: str):
        """Инициализация потока

        Args:
            socket (socket.socket): сокет, на котором слушает клиент
            address (str): адрес клиента
        """
        super().__init__()
        # Создаем адаптер для работы с сокетом и разбора запросов
        self._socket: SocketAdapter = SocketAdapter(socket)
        self._address: str = address
        self.request: SocketRequest = None

    def getalglist(self) -> SocketResponse:
        """Обработчик запроса алгоритмов

        Args:
            request (SocketRequest)

        Returns:
            SocketResponse
        """
        response = SocketResponse()
        response.payload = "\n".join(x.stem for x in alg_dir.rglob("*.py") 
                                     if x.name != "__init__.py").encode()
        return response
   
    def echo(self) -> SocketResponse:
        """Обработчик команды echo
            Возвращает представление переданных данных 
        Args:
            request (SocketRequest)

        Returns:
            SocketResponse
        """
        response = SocketResponse()
        response.payload = f"command={self.request.command}\nparams:\n\t" +\
                             "\n\t".join(f"{k} = {v}" for k, v in self.request.params.items()) +\
                             f"\npayload length: {len(self.request.payload)}".encode()
        return response

    def unknown(self) -> SocketResponse:
        """Обработчик неизвестной команды

        Args:
            request (SocketRequest)

        Returns:
            SocketResponse
        """
        return SocketResponse(SERVER_UNKNOWN, f"Неизвестная команда {self.request.command}")

    def info(self, message: str, info: bool = True) -> None:
        """ Вывод логгера
            Добавляет в вывод адрес клиента
        Args:
            message (str): сообщение
            info (bool, optional): уровень отладки
        """
        str_message = f"{self._address[0]}:{self._address[1]}: {message}"
        if info: 
            logger.info(str_message)
        else: 
            logger.debug(str_message)

    def _load_module(self, alg_name: str) -> ModuleType:
        """Загрузка модуля обработки алгоритма
        Args:
            alg_name (str): имя модуля
        Raises:
            ImportError:
        Returns:
            ModuleType - модуль алгоритма кодирования
        """
        # Загрузка модуля по указанному имени
        module_name = f"alg.{alg_name}"
        self.info(f"Importing module {module_name}")
        if module_name in sys.modules:
            module = sys.modules[module_name]
        else:
            try:
                module =  importlib.import_module(module_name)
            except Exception as e:
                raise ImportError(f"Не удалось загрузить модуль {alg_name}: {str(e)}")    
        # Проверка существования методов кодирования и раскодирования
        if (not hasattr(module, "encode")) or (not hasattr(module, "decode")):
            raise ImportError(f"Модуль {alg_name} не содержит нужных функций")
        return module

    def check_alg(self) -> SocketResponse:           
        """ Проверка загрузки алгоритма и наличия в нем нужных функций

        Args:
            request (SocketRequest): _description_

        Returns:
            SocketResponse: _description_
        """
        try:
            alg_name = self.request.params["alg_name"]
            _ = self._load_module(alg_name)
        except IndexError:
            return SocketResponse(SERVER_BAD_REQUEST, "Не найден параметр alg_name с указанием алгоритма")
        except Exception as e:
            return SocketResponse.error_response(f"Ошибка загрузки модуля {alg_name}:\n{str(e)}")
        return SocketResponse()

    def process_data(self, encode: bool = True) -> SocketResponse:
        """Обработка команд кодирования и декодирования данных

        Args:
            request (SocketRequest): Запрос
            encode (bool, optional): Признак - кодировать или декодировать. По умолчанию - кодировать

        Returns:
            SocketResponse: _description_
        """
        # Проверка корретности запроса
        if (self.request.params == None) or ("alg_name" not in self.request.params):
            return SocketResponse(SERVER_BAD_REQUEST, "Не найден параметр alg_name с указанием алгоритма")
        if not self.request.payload:
            return SocketResponse(SERVER_BAD_REQUEST, "В запросе отсутсвет информация для обработки")
        try:
            module = self._load_module(self.request.params["alg_name"])
            if encode:
                func = module.encode
            else:
                func = module.decode
            # Обработка данных
            self.info(f"Coding data")
            output = func(self.request.payload)
            self.info(f"Encoded/decoded data length: {len(output)}")
            return SocketResponse(SERVER_OK, "", output)
        except Exception as e:
            return SocketResponse.error_response(str(e))

    def run(self):
        """Основной обработчик потока
        """
        self.info("Connected client")
        try:
            # Слушаем до тех пор, пока есть запросы
            while True:
                self.request = self._socket.get_request()
                self.info(f"Command: {self.request.command}")
                # Формируем ответ в зависимости от команды
                match self.request.command:
                    # Список алгоритмов
                    case "list": 
                        response = self.getalglist()
                    # Проверка загрузки алгоритма и наличия в нем нужных функций
                    case "check": 
                        response = self.check_alg()
                    # Эхо
                    case "echo":
                        response = self.echo()
                        self.info(response.payload.decode())
                    # Завершение соединения
                    case "close": 
                        self.info("Disconnect")
                        break
                    # Кодирование данных
                    case "encode": 
                        response = self.process_data(encode=True)
                    # Декодирование данных
                    case "decode": 
                        response = self.process_data(encode=False)
                    # Неизвестная команда
                    case _ :
                        response = self.unknown()
                self._socket.send_response(response)
        except Exception as e:
            # Если что-то пошло не так, то отправляем сообщение ошибки. Напоследок
            logger.error(str(e))
        finally:
            # Закрыть сокет по завершении работы
            self._socket.close()

def setup(filename: str) -> None:
    """Чтение настроек из файла

    Args:
        filename (str): файл настроек
    """
    global PORT, MAX_CONNECTIONS, BUF_SIZE

    def _get_int(name: str, default_value: int) -> int:
        """Преобразование значения параметрв в целое, возвращает default_value - если ошибка или параметр не найден"""
        try:
            return int(config[name])
        except:
            return default_value
        
    # Читаем настройки из файла в словарь
    config_file: Path = Path(module_dir / filename)
    config = dict()
    if config_file.is_file():
        for line in config_file.read_text().splitlines():
            if "=" in line:
                k, v = map(str.strip, line.split("=", maxsplit=1))
                config[k.upper()] = v
            else: 
                config[line.strip()] = None

    # Порт, на котором будем работать
    PORT = _get_int("PORT", PORT)
    # Максимальное количество соединений
    MAX_CONNECTIONS = _get_int("MAX_CONNECTIONS", MAX_CONNECTIONS)
    
    # Настройка логгера
    logger.setLevel(logging.DEBUG  if "DEBUG" in config else logging.INFO)
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    logger.addHandler(ch)            


if __name__ == "__main__":
    # Загрузка настроек
    setup("config.cfg")
    with socket.socket() as sock:
        # Соединяемся с сокетом
        sock.bind(("", PORT))
        # Слушаем сокет
        sock.listen(MAX_CONNECTIONS)
        while True:
            # Получили соединения
            conn, addr = sock.accept()
            # Запустили поток обработки
            th = Worker(conn, addr)
            th.start()