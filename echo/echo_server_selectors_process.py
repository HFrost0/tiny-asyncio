import socket
import selectors
import multiprocessing as mp

from echo.base_server import cpu_bound_task
from echo.echo_server_selectors import SelectorsServer


class SelectorsProcessServer(SelectorsServer):
    def __init__(self, address, cpu=False, num_workers=4):
        super(SelectorsProcessServer, self).__init__(address, cpu)
        self.num_workers = num_workers

    def start_sering(self):
        sema1 = mp.Semaphore(0)
        sema2 = mp.Semaphore(0)
        for i in range(self.num_workers):
            mp.Process(target=worker, args=(self.listener, sema1, sema2, self.cpu)).start()
        while True:
            self.sel.select()  # block waiting for connect
            sema1.release()
            sema2.acquire()


def worker(server: socket.socket, sema: mp.Semaphore, sema2: mp.Semaphore, cpu):
    sel = selectors.DefaultSelector()
    while True:
        if sema.acquire(block=len(sel.get_map()) == 0):  # block if no fileno is registered
            client, addr = server.accept()
            sema2.release()
            client.setblocking(False)
            sel.register(client.fileno(), selectors.EVENT_READ, data=client)
            print(f"Connection: {addr}")
        event_list = sel.select(timeout=0)  # todo nonblocking since we need worker to accept new connection
        for key, mask in event_list:
            client = key.data
            # echo
            if data := client.recv(1024):
                client.send(data)
                if cpu:
                    cpu_bound_task()  # cpu bound task
                print(f'Echo {data}')
            else:
                sel.unregister(client.fileno())
                client.close()
                print(f'Remove: {client}')


if __name__ == '__main__':
    server = SelectorsProcessServer(('127.0.0.1', 6666), cpu=True)
    server.start_sering()
