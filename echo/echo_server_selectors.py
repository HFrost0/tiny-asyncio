import socket
import selectors

from echo.base_server import BaseServer


class SelectorsServer(BaseServer):
    def __init__(self, address, cpu=False):
        super(SelectorsServer, self).__init__(address=address, cpu=cpu)
        self.listener.setblocking(False)
        self.sel = selectors.DefaultSelector()
        self.sel.register(self.listener.fileno(), selectors.EVENT_READ, data=self.listener)

    def accept_client(self):
        sock, addr = self.listener.accept()
        sock.setblocking(False)
        self.sel.register(sock.fileno(), selectors.EVENT_READ, data=sock)
        print(f"Connection: {addr}")

    def detach_client(self, sock: socket.socket):
        self.sel.unregister(sock.fileno())
        sock.close()
        print(f'Remove: {sock}')

    def start_sering(self):
        while True:
            event_list = self.sel.select()  # control
            for key, mask in event_list:
                sock = key.data
                if sock is self.listener:
                    self.accept_client()
                else:
                    if data := sock.recv(1024):
                        self.echo(sock, data)
                    else:
                        self.detach_client(sock)


if __name__ == '__main__':
    server = SelectorsServer(("127.0.0.1", 6666))
    server.start_sering()
