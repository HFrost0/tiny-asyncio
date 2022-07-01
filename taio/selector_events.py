import functools
import heapq
import selectors
import socket
from collections import deque
import time
from . import tasks, futures


class EventLoop:
    def __init__(self):
        self._ready = deque()
        self._scheduled = []
        self._stopping = False
        self._selector = selectors.DefaultSelector()

    def call_soon(self, callback, *args):
        self._ready.append((callback, args))

    def call_later(self, delay, callback, *args):
        t = time.time() + delay
        heapq.heappush(self._scheduled, (t, callback, args))

    def stop(self):
        self._stopping = True

    def run_forever(self):
        while True:
            self.run_once()
            if self._stopping:
                break
            # print('Event loop run once')

    def run_once(self):
        # select and block here
        timeout = None  # None means wait forever until some fd is ready
        if self._ready or self._stopping:
            timeout = 0
        elif self._scheduled:
            when = self._scheduled[0][0]
            timeout = when - time.time()

        event_list = self._selector.select(timeout)
        # process event list
        for key, mask in event_list:
            # fileobj, (reader, writer) = key.fileobj, key.data
            cb, args = key.data
            self._ready.append((cb, args))

        while self._scheduled and self._scheduled[0][0] < time.time():  # at least one schedule
            _, cb, args = heapq.heappop(self._scheduled)
            self._ready.append((cb, args))

        num = len(self._ready)
        # for i, (cb, args) in enumerate(self._ready):
        #     print(i, 'cb:', cb, 'args:', args)
        for i in range(num):
            cb, args = self._ready.popleft()
            cb(*args)  # run callback

    def add_writer(self, fd, callback, *args):
        self._selector.register(fd, selectors.EVENT_WRITE, data=(callback, args))
        # return callback

    def remove_writer(self, fd):
        self._selector.unregister(fd)

    def add_reader(self, fd, callback, *args):
        self._selector.register(fd, selectors.EVENT_READ, data=(callback, args))
        # return callback

    def remove_reader(self, fd):  # todo distinguish read and write
        self._selector.unregister(fd)

    async def sock_recv(self, sock, n):
        try:
            return sock.recv(n)
        except BlockingIOError:
            pass
        fut = self.create_future()
        self.add_reader(sock.fileno(), self._sock_recv, fut, sock, n)
        fut.add_done_callback(functools.partial(self._sock_read_done, sock.fileno()))
        return await fut

    def _sock_recv(self, fut, sock, n):
        if fut.done():
            return
        try:
            data = sock.recv(n)
        except BlockingIOError:
            return  # try again next time
        except BaseException as exc:
            fut.set_exception(exc)
        else:
            fut.set_result(data)

    def _sock_read_done(self, fd, fut):
        self.remove_reader(fd)

    def _sock_write_done(self, fd, fut):
        self.remove_writer(fd)

    async def sock_connect(self, sock, address):
        """just create a sock and wait for connected"""
        fut = self.create_future()
        try:
            sock.connect(address)
        except BlockingIOError:
            # once fd is writeable, set future done
            self.add_writer(sock.fileno(), self._sock_connect_cb, fut, sock, address)
            # once writeable, unregister fd
            fut.add_done_callback(functools.partial(self._sock_write_done, sock.fileno()))
        except BaseException as exc:
            fut.set_exception(exc)
        else:
            fut.set_result(None)
        return await fut

    def _sock_connect_cb(self, fut, sock, address):
        if fut.done():
            return  # todo asyncio use cancel to avoid this
        try:
            err = sock.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
            if err != 0:
                # Jump to any except clause below.
                raise OSError(err, f'Connect call failed {address}')
        except BlockingIOError:
            # socket is still registered, the callback will be retried later
            pass
        except BaseException as exc:
            fut.set_exception(exc)
        else:
            fut.set_result(None)

    async def sock_accept(self, sock):
        try:
            conn, address = sock.accept()
            conn.setblocking(False)
            return conn, address
        except BlockingIOError:
            fut = self.create_future()
            self.add_reader(sock.fileno(), self._sock_accept, fut, sock)
            fut.add_done_callback(functools.partial(self._sock_read_done, sock.fileno()))
        return await fut

    def _sock_accept(self, fut, sock):
        if fut.done():
            return
        try:
            conn, address = sock.accept()
            conn.setblocking(False)
        except BlockingIOError:
            pass
        except BaseException as exc:
            fut.set_exception(exc)
        else:
            fut.set_result((conn, address))

    def create_task(self, coro):
        task = tasks.Task(coro, loop=self)
        return task

    def create_future(self):
        fut = futures.Future(loop=self)
        return fut

    def run_until_complete(self, coro):
        # todo type check... ensure future
        future = self.create_task(coro)
        future.add_done_callback(_run_until_complete_cb)

        self.run_forever()

        return future.result()


def _run_until_complete_cb(fut):
    fut.get_loop().stop()
