"""
🙄 not very efficient...
"""
import socket
import selectors
import multiprocessing as mp

from echo.base_server import cpu_bound_task, BaseServer


class SelectorsProcess2Server(BaseServer):
    def __init__(self, address, cpu=False, num_workers=4):
        super(SelectorsProcess2Server, self).__init__(address, cpu)
        self.num_workers = num_workers
        self.lock = mp.Lock()

    def start_serving(self):
        workers = []
        for i in range(self.num_workers):
            p = mp.Process(target=worker, args=(self.listener, self.lock, self.cpu))
            p.start()
            workers.append(p)
        for p in workers:
            p.join()


def worker(server: socket.socket, lock: mp.Lock, cpu=False):
    # lock = mp.Lock()
    sel = selectors.DefaultSelector()
    sel.register(server.fileno(), selectors.EVENT_READ, data=server)
    while True:
        event_list = sel.select()
        for key, mask in event_list:
            sock = key.data
            if sock is server:
                if lock.acquire(block=False):
                    client, addr = server.accept()
                    lock.release()
                    client.setblocking(False)
                    sel.register(client.fileno(), selectors.EVENT_READ, data=client)
                    print(f"Connection: {addr}")
            else:
                if data := sock.recv(1024):
                    sock.send(data)
                    if cpu:
                        cpu_bound_task()  # cpu bound task
                    print(f'Echo {data}')
                else:
                    sel.unregister(sock.fileno())
                    sock.close()
                    print(f'Remove: {sock}')


if __name__ == '__main__':
    server = SelectorsProcess2Server(('127.0.0.1', 6666), cpu=True)
    server.start_serving()
