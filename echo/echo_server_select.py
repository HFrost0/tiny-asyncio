import socket
import select

from echo.base_server import BaseServer


class SelectServer(BaseServer):
    def __init__(self, address, cpu=False):
        super(SelectServer, self).__init__(address, cpu)
        self.readers = [self.listener]

    def accept_client(self):
        client, addr = self.listener.accept()
        client.setblocking(False)
        self.readers.append(client)
        print(f'Connection: {addr}')

    def detach_client(self, sock: socket.socket):
        sock.close()
        self.readers.remove(sock)
        print(f'Remove: {sock}')

    def start_serving(self):
        while True:
            readable, writeable, errored = select.select(self.readers, [], [])
            # readable, writeable, errored = select.select(readers, [], [], 0.5)  # this will run once every 0.5 sec
            for s in readable:
                if s is self.listener:
                    self.accept_client()
                else:  # client want to send to server
                    if data := s.recv(1024):
                        self.echo(s, data)
                    else:
                        self.detach_client(s)


if __name__ == '__main__':
    server = SelectServer(('', 6666))
    server.start_serving()
