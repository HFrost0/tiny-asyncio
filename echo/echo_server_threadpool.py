from concurrent.futures import ThreadPoolExecutor

from echo.echo_server_thread import ThreadServer


class ThreadPoolServer(ThreadServer):
    def __init__(self, address=("127.0.0.1", 6666), cpu=False):
        super(ThreadPoolServer, self).__init__(address, cpu)
        self.pool = ThreadPoolExecutor()

    def start_sering(self):
        while True:
            s, addr = self.listener.accept()
            print(f'Connection: {addr}')
            self.pool.submit(self.handler, s)


if __name__ == '__main__':
    server = ThreadPoolServer()
    server.start_sering()
