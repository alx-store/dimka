import socket

BUF_SIZE = 4096
SEPARATOR = b"~EOP~"
END_MESSAGE_TEXT = b"~EOM~"

SERVER_OK = 0
SERVER_ERROR = 1
SERVER_UNKNOWN = 2
SERVER_BAD_REQUEST = 3

class SocketRequest:
    """ Запрос серверу
        Формат запроса:
        <комманда>~EOP~<параметры>~EOP~<payload>~EOM~"
        <комманда> - команда серверу на выполнение действия
        <параметры> - параметры команды в формате: key_1=value_1;...key_n=value_n
        <payload> - данные для обработки (bytes)
    """

    def get_params(self, params_str: str) -> None:
        """ Формирует словарь параметров из строки
        Args:
            params_str (str): строка параметров формата: key_1=value_1;...key_n=value_n
        """
        if params_str:
            for x in params_str.split(";"):
                if "=" in x:
                    k, v = x.split("=", maxsplit=1)
                    self.params[k.strip()] = v.strip()
                else:
                    self.params[x.strip()] = None

    def __init__(self, command: str = None, params: dict = None, payload: bytes = None) -> None:
        self.command = command
        self.params = params or dict()
        self.payload = payload

    @staticmethod
    def from_data(data: bytes) -> "SocketRequest":
        """Генерирует запрос из массива байт. Преобразует данные полученные из сокета в запрос
        Args:
            data (bytes): массив байт

        Returns:
            SocketRequest
        """
        parts = data.split(SEPARATOR, maxsplit=2)
        request = SocketRequest()
        request.command = parts[0].decode().lower()
        request.get_params(parts[1].decode())
        request.payload = parts[2]
        return request


class SocketResponse:
    """ Ответ сервера
        Формат ответа: <code>~EOP~<message>~EOP~payload~EOM~
        code - код ответа, 0 - если команда обработана успешно
        message - текстовое сообщение
        payload - обработанные данные
    """
    def __init__(self, code: int = 0, message: str = "", payload: bytes = None ) -> None:
        self.code = code
        self.message = message
        self.payload = payload
    
    def check_status(self) -> None:
        """Проверяет статус, генерирует исключение с сообщение об ошибке, если статус не SERVER_OK
        """
        if self.code != SERVER_OK:
            raise Exception(self.message)

    @staticmethod
    def error_response(message: str) -> "SocketResponse":
        """ Возвращает ответ сервера об ошибке

        Args:
            message (str): сообщение об ошибке

        Returns:
            SocketResponse
        """
        return SocketResponse(SERVER_ERROR, message)

    @staticmethod
    def from_data(data: bytes)  -> "SocketResponse":
        """ Формирует ответ по данным полученным из сокета

        Args:
            data (bytes): _description_

        Returns:
            SocketResponse: _description_
        """
        parts = data.split(SEPARATOR, maxsplit=2)
        response = SocketResponse()
        try:
            response.code = int(parts[0].decode())
            response.message = parts[1].decode()
            response.payload = parts[2]
        except Exception as e:
            return SocketResponse.error_response(str(e))

        return response


class SocketAdapter:
    """ Адаптер для сокета
        Реализует отправку и получение запросов и ответов
    """
    def __init__(self, sock: socket.socket) -> None:
        self._socket: socket.socket = sock
    
    def _get_from_socket(self) -> bytes:
        """Получение данных из сокета

        Returns:
            bytes: полученные из сокета данные
        """
        data = b""
        # Читаем из сокета до тех пор пока полученные данные не заканчиваются на строку END_MESSAGE_TEXT
        while not data.endswith(END_MESSAGE_TEXT):
            # Данные считываем порциями по BUF_SIZE байт
            buffer = self._socket.recv(BUF_SIZE)
            if not buffer:
                break
            # Полученную порцию добавляем к общему результату
            data += buffer
        # Возвращаем массив байт, но уже без END_MESSAGE_TEXT
        return data[:-len(END_MESSAGE_TEXT)]
    
    def get_request(self) -> SocketRequest:
        """ Получение запроса из сокета
        Returns:
            SocketRequest
        """
        return SocketRequest.from_data(self._get_from_socket())

    def get_response(self) -> SocketResponse:
        """ Получение ответа из сокета
        Returns:
            SocketResponse
        """
        return SocketResponse.from_data(self._get_from_socket())

    def send_request_header(self, command: str, params: dict = None) -> None:
        """ Отправка запроса в сокет - без данных для обработки

        Args:
            command (str): _description_
            params (dict, optional): _description_. Defaults to None.
        """
        # Отправка команды
        self._socket.send(command.encode())
        # Разделитель
        self._socket.send(SEPARATOR)
        # Если есть параметры, то формируем строку и отправляем
        if params and len(params) > 0:
            str_params = ";".join(f"{k}={v}" for k, v in params.items())
            self._socket.send(str_params.encode())
        # Разделитель
        self._socket.send(SEPARATOR)

    def send_data(self, data: bytes) -> None:
        """Отправка данных в сокет
        Args:
            data (bytes): данные для отправки
        """
        self._socket.sendall(data)
        # Признак конца сообщения вызывающая сторона должна отправлять самостоятельно - на случай, если нужно отправлять файл по частям
        
    def send_request(self, request: SocketRequest) -> None:
        """Отправка запроса в сокет

        Args:
            request (SocketRequest): Запрос
        """
        # Отправка заголовка
        self.send_request_header(request.command, request.params)
        # Если есть данные для обработки, то отправляем
        if request.payload:
            self._socket.sendall(request.payload)
        # Конец сообщения
        self.end_message()

    def send_response_header(self, code: int, message: str = None) -> None:
        """Отправка заголовка ответа в сокет
        Args:
            code (int): код ответа
            message (str, optional): сообщение (опционально)
        """
        self._socket.send(str(code).encode())
        self._socket.send(SEPARATOR)
        if message:
            self._socket.send(message.encode())
        self._socket.send(SEPARATOR)

    def send_response(self, response: SocketResponse) -> None:
        """Отправка ответа в сокет

        Args:
            response (SocketResponse): Ответ сервера
        """
        self.send_response_header(response.code, response.message)
        # Если есть обработанные данные, то отправляем
        if response.payload:
            self._socket.sendall(response.payload)
        # Конец сообщения
        self.end_message()
    
    def end_message(self):
        """Отправка маркера конца сообщения
        """
        self._socket.send(END_MESSAGE_TEXT)

    def close(self) -> None:
        """Закрывает сокет
        """
        self._socket.close()

class ClientAdapter(SocketAdapter):
    """Адаптер для клиента
       Наследует от  SocketAdapter, упрощает получение ответа на запрос
    Args:
        SocketAdapter (_type_): _description_
    """
    def get(self, request: SocketRequest) -> SocketResponse:
        """Отправить запрос и получить ответ
        Args:
            request (SocketRequest): Запрос

        Returns:
            SocketResponse
        """
        try:
            self.send_request(request)
            return(self.get_response())
        except Exception as e:
            # Если произошла ошибка отправить сообщение об ошибке
            return SocketResponse.error_response(str(e))

    def close(self) -> None:
        """Закрывает сокет
        """
        self.send_request(SocketRequest("close"))
        super().close()

    