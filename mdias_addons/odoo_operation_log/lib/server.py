import threading
from .management import LogManage


class LogServer(threading.Thread):

    def run(self) -> None:
        while True:
            LogManage.handler()


server = LogServer()
server.start()
