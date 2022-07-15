"""
DO NOT use this server for c10k test!
"""
import socket
import threading

from echo.base_server import BaseServer


class ThreadServer(BaseServer):
    def start_serving(self):
        while True:
            s, addr = self.listener.accept()
            print(f'Connection: {addr}')
            threading.Thread(target=self.handler, args=(s,)).start()

    def handler(self, s: socket.socket):
        while data := s.recv(1024):
            self.echo(s, data)
        s.close()
        print(f'Remove: {s}')


if __name__ == '__main__':
    server = ThreadServer(("127.0.0.1", 6666))
    server.start_serving()
