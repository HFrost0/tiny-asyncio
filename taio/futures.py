from . import events


class Future:
    # Class variables serving as defaults for instance variables.
    _done = False
    _result = None
    _exception = None

    def __init__(self, loop=None):
        self._loop = loop if loop is not None else events.get_event_loop()
        self._callbacks = []

    def done(self):
        return self._done

    def get_loop(self):
        return self._loop

    def result(self):
        if not self._done:
            raise Exception('Future not done yet')
        if self._exception is not None:
            raise self._exception
        return self._result

    def exception(self):
        if not self._done:
            raise Exception('Future not done yet')
        return self._exception

    def __schedule_callbacks(self):
        for cb in self._callbacks:
            self._loop.call_soon(cb, self)
        self._callbacks = []  # clear all callbacks

    def set_result(self, result):
        if self._done:
            raise Exception('Future is done')
        self._result = result
        self._done = True
        self.__schedule_callbacks()

    def set_exception(self, exception):
        if self._done:
            raise Exception('Future is done')
        self._exception = exception
        self._done = True
        self.__schedule_callbacks()
        # traceback

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
