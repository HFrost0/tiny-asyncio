import heapq
from collections import deque
import time
from tasks import Task


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
        task = Task(coro, loop=self)
        return task

    def run_until_complete(self, coro):
        # todo type check... ensure future
        future = self.create_task(coro)
        future.add_done_callback(_run_until_complete_cb)

        self.run_forever()

        return future.result()


def _run_until_complete_cb(fut):
    fut.get_loop().stop()


loop = EventLoop()

# todo get_running_loop
