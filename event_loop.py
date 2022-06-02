import heapq
from collections import deque
import time


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
            time.sleep(0.1)
            print('Event loop run once')

    def run_once(self):
        now = time.time()
        while self._scheduled and self._scheduled[0][0] < now:  # at least one schedule
            _, cb, args = heapq.heappop(self._scheduled)
            self._ready.append((cb, args))

        num = len(self._ready)
        for i in range(num):
            cb, args = self._ready.popleft()
            cb(*args)  # run callback
