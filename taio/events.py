import heapq
import threading
from collections import deque
import time
from . import tasks


class EventLoop:
    def __init__(self):
        self._ready = deque()
        self._scheduled = []
        self._stopping = False

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
            time.sleep(0.1)  # avoid high cpu usage by now
            print('Event loop run once')

    def run_once(self):
        now = time.time()
        # todo learn selectors and block the event loop here just like asyncio
        while self._scheduled and self._scheduled[0][0] < now:  # at least one schedule
            _, cb, args = heapq.heappop(self._scheduled)
            self._ready.append((cb, args))

        num = len(self._ready)
        for i in range(num):
            cb, args = self._ready.popleft()
            cb(*args)  # run callback

    def create_task(self, coro):
        task = tasks.Task(coro, loop=self)
        return task

    def run_until_complete(self, coro):
        # todo type check... ensure future
        future = self.create_task(coro)
        future.add_done_callback(_run_until_complete_cb)

        self.run_forever()

        return future.result()


class EventLoopPolicy:
    _loop_factory = EventLoop

    class _Local(threading.local):  # 😅
        _loop = None
        _set_called = False

    def __init__(self):
        self._local = self._Local()

    def get_event_loop(self):
        if self._local._loop is None and not self._local._set_called \
                and threading.current_thread() is threading.main_thread():
            self.set_event_loop(self.new_event_loop())
        if self._local._loop is None:
            raise RuntimeError('There is no current event loop in thread %r.'
                               % threading.current_thread().name)
        return self._local._loop

    def new_event_loop(self):
        return self._loop_factory()

    def set_event_loop(self, loop):
        self._local._set_called = True
        assert loop is None or isinstance(loop, EventLoop)
        self._local._loop = loop


_event_loop_policy = None
_lock = threading.Lock()


def get_event_loop_policy():
    global _event_loop_policy
    with _lock:
        if _event_loop_policy is None:
            _event_loop_policy = EventLoopPolicy()
    return _event_loop_policy


def get_event_loop():
    # _get_running_loop()
    return get_event_loop_policy().get_event_loop()


def _run_until_complete_cb(fut):
    fut.get_loop().stop()
