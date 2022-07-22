import socket
from concurrent.futures import ProcessPoolExecutor

from echo.base_server import cpu_bound_task
from echo.echo_server_selectors import SelectorsServer


class SelectorsProcessServer(SelectorsServer):
    def __init__(self, address, cpu=False):
        super(SelectorsProcessServer, self).__init__(address, cpu)
        self.pool = ProcessPoolExecutor()

    def echo(self, sock: socket.socket, data: bytes):
        sock.send(data)
        if self.cpu:
            self.pool.submit(cpu_bound_task).result()  # this can not speed up!
        print(f'Echo {data}')


if __name__ == '__main__':
    server = SelectorsProcessServer(("127.0.0.1", 6666), cpu=True)
    server.start_serving()
