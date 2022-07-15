import socket


def cpu_bound_task():
    sum(range(100000))


class BaseServer:
    def __init__(self, address: tuple, cpu=False):
        self.cpu = cpu
        self.listener = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.listener.bind(address)
        self.listener.listen()

    def echo(self, sock: socket.socket, data: bytes):
        sock.send(data)
        if self.cpu:
            cpu_bound_task()  # cpu bound task
        print(f'Echo {data}')

    def start_sering(self):
        raise NotImplemented
