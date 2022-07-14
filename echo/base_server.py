import socket


class BaseServer:
    def __init__(self, address):
        self.listener = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.listener.bind(address)
        self.listener.listen()

    def start_sering(self):
        raise NotImplemented

