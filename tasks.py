from futures import Future
import event_loop


class Task(Future):
    def __init__(self, coro):
        super().__init__()
        self._coro = coro
        self._loop.call_soon(self.__step)

    def __step(self):
        if self._done:
            raise Exception('Task all ready done')
        try:
            result = self._coro.send(None)
        except StopIteration as exc:
            super().set_result(exc.value)
        else:
            result.add_done_callback(self.__step)


async def sleep(delay):
    future = Future()
    event_loop.loop.call_later(delay, future.set_result, None)
    return await future
