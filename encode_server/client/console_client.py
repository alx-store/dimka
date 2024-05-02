import sys
import socket
from pathlib import Path

module_dir = Path(__file__).parent
sys.path.append(str(module_dir.parent))

from common.protocol import *

client = socket.socket()            # создаем сокет клиента
hostname = "127.0.0.1"     # получаем хост локальной машины
port = 10001                        # устанавливаем порт сервера
client.connect((hostname, port))    # подключаемся к серверу
adapter = ClientAdapter(client)
try:
    rsp = adapter.get(SocketRequest("list"))
    print(rsp.payload.decode())
    rsp = adapter.get(SocketRequest("ldasdadist"))
    print(rsp.message)
    adapter.send_request(SocketRequest("close"))
except socket.timeout:
    print("send data timeout")
except socket.error as ex:
    print("send data error:", ex)