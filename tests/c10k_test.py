import socket
import time

import taio


async def client_send(sock, client_id, send_times=100):
    loop = taio.get_event_loop()
    data = []
    for i in range(send_times):  # say multiple times
        sock.send(f"{client_id} taio client say {i}".encode('utf8'))
        data.append(await loop.sock_recv(sock, 1024))
    sock.close()
    # print(data)


async def test_once(port=6666, num_clients=1000, send_times=100):
    cors = []
    start = time.monotonic()
    for i in range(num_clients):
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        sock.connect(('127.0.0.1', port))  # sync connect
        sock.setblocking(False)
        cors.append(client_send(sock, i, send_times))
    conn_time = time.monotonic() - start
    start = time.monotonic()
    await taio.gather(*cors, return_exceptions=False)
    echo_time = time.monotonic() - start
    return conn_time, echo_time


async def test_avg(port=6666, num_clients=1000, send_times=100, test_times=1):
    cts, ets = [], []
    for _ in range(test_times):
        ct, et = await test_once(port, num_clients, send_times)
        cts.append(ct)
        ets.append(et)
        print(f"Connect time: {ct}, Echo time: {et}")
    print(f"Average Connect time: {sum(cts) / len(cts)}, Echo time: {sum(ets) / len(ets)}")


if __name__ == '__main__':
    loop = taio.get_event_loop()
    loop.run_until_complete(test_avg(num_clients=10000, send_times=1))
