import socket
from concurrent.futures import ThreadPoolExecutor

from echo.base_server import BaseServer


class ThreadPoolServer(BaseServer):
    def __init__(self, address=("127.0.0.1", 6666)):
        super(ThreadPoolServer, self).__init__(address)
        self.pool = ThreadPoolExecutor()

    def start_sering(self):
        while True:
            s, addr = self.listener.accept()
            print(f'Connection: {addr}')
            self.pool.submit(self.handler, s)

    def handler(self, sock: socket.socket):
        while data := sock.recv(1024):
            sock.send(data)
            # sum(range(100000))  # slow down respond
            print(f'Echo: {data}')
        sock.close()
        print(f'Remove: {sock}')


if __name__ == '__main__':
    server = ThreadPoolServer()
    server.start_sering()
