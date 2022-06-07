import event_loop


class Future:
    _done = False
    _result = None
    _loop = event_loop.loop  # global loop for all future

    def __init__(self):
        self._callbacks = []

    def result(self):
        if not self._done:
            raise Exception('Future not done yet')
        return self._result

    def set_result(self, result):
        if self._done:
            raise Exception('Future is done')
        self._result = result
        self._done = True
        for cb in self._callbacks:
            self._loop.call_soon(cb, self)

    def add_done_callback(self, fn):
        if self._done:
            self._loop.call_soon(fn)
        else:
            self._callbacks.append(fn)

    def __await__(self):
        if not self._done:
            yield self
        return self._result

    __iter__ = __await__


if __name__ == '__main__':
    a = Future()
    b = Future()
