import random
import socket
import time

import taio


async def client_send(sock, client_id):
    loop = taio.get_event_loop()
    # await taio.sleep(random.random())
    data = []
    for i in range(100):  # say multiple times
        sock.send(f"{client_id} taio client say {i}".encode('utf8'))
        data.append(await loop.sock_recv(sock, 1024))
    sock.close()
    print(data)


async def main(port):
    cors = []
    start = time.time()
    for i in range(10000):
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        sock.connect(('127.0.0.1', port))  # sync connect
        sock.setblocking(False)
        cors.append(client_send(sock, i))
    print(f"Connect time: {time.time() - start}")
    start = time.time()
    await taio.gather(*cors, return_exceptions=True)
    print(f'All done, time: {time.time() - start}')


if __name__ == '__main__':
    loop = taio.get_event_loop()
    loop.run_until_complete(main(6666))
