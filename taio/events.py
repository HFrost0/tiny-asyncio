import threading
from .selector_events import *


class EventLoopPolicy:
    _loop_factory = EventLoop

    class _Local(threading.local):  # 😅
        _loop = None
        _set_called = False

    def __init__(self):
        self._local = self._Local()

    def get_event_loop(self) -> EventLoop:
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


def get_event_loop_policy() -> EventLoopPolicy:
    global _event_loop_policy
    with _lock:
        if _event_loop_policy is None:
            _event_loop_policy = EventLoopPolicy()
    return _event_loop_policy


def get_event_loop():
    # _get_running_loop()
    return get_event_loop_policy().get_event_loop()
