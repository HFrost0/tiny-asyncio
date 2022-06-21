from . import futures
from . import events


class Task(futures.Future):
    def __init__(self, coro, loop=None):
        super().__init__(loop=loop)
        self._coro = coro
        self._loop.call_soon(self.__step)

    def __step(self):
        if self.done():
            raise Exception('Task all ready done')
        try:
            result = self._coro.send(None)  # result is the future object yield from bottom
        except StopIteration as exc:
            super().set_result(exc.value)
        else:
            # current task is waiting result to complete,
            # just add a callback on that future and disappear in event loop
            result.add_done_callback(self.__wakeup)

    def __wakeup(self, future):
        # future is the "father"
        try:
            future.result()
        except BaseException as exc:
            # self.__step(exc)
            print(exc)
            raise  # raise since future is not done yet
        else:
            self.__step()


async def sleep(delay):
    future = futures.Future()
    events.get_event_loop().call_later(delay, future.set_result, None)
    return await future  # yield a empty future
