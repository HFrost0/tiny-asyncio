import event_loop


class Future:
    _done = False
    _result = None

    def __init__(self, loop=None):
        self._loop = loop if loop is not None else event_loop.loop
        self._callbacks = []

    def get_loop(self):
        return self._loop

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
        self._callbacks = []  # clear callbacks

    def add_done_callback(self, fn):
        """
        🌟 The callback is always called with a single argument - the future object.
        """
        if self._done:
            self._loop.call_soon(fn, self)
        else:
            self._callbacks.append(fn)

    def __await__(self):
        if not self._done:
            yield self
        return self.result()

    __iter__ = __await__


if __name__ == '__main__':
    a = Future()
    b = Future()
