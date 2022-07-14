import socket
import selectors
import multiprocessing as mp


def worker(server: socket.socket, sema: mp.Semaphore, sema2: mp.Semaphore):
    sel = selectors.DefaultSelector()
    while True:
        state = sema.acquire(block=len(sel.get_map()) == 0)  # block if no fileno is registered
        if state:
            client, addr = server.accept()
            client.setblocking(False)
            sel.register(client.fileno(), selectors.EVENT_READ, data=client)
            print(f"Connection: {addr}")
            sema2.release()
        event_list = sel.select(timeout=0)  # todo nonblocking since we need worker to accept new connection
        for key, mask in event_list:
            client = key.data
            # echo
            data = client.recv(1024)
            if data:
                client.send(data)
                # sum(range(100000))  # cpu bound task
                print(f'Echo {data}')
            else:
                sel.unregister(client.fileno())
                client.close()
                print(f'Remove: {client}')


def startup_server(address, worker_num=4):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(address)
    server.listen()
    server.setblocking(False)

    sel = selectors.DefaultSelector()
    sema = mp.Semaphore(0)
    sema2 = mp.Semaphore(0)
    for i in range(worker_num):
        mp.Process(target=worker, args=(server, sema, sema2)).start()
    sel.register(server.fileno(), selectors.EVENT_READ, )
    while True:
        sel.select()  # block waiting for connect
        sema.release()
        sema2.acquire()


if __name__ == '__main__':
    startup_server(('127.0.0.1', 6666))
