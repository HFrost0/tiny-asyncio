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
            result = self._coro.send(None)  # result is the future object yield from bottom
        except StopIteration as exc:
            super().set_result(exc.value)
        else:
            result.add_done_callback(self.__wakeup)  # current task is waiting result so

    def __wakeup(self, future):
        # future is the "father"
        try:
            future.result()
        except BaseException as exc:
            # self.__step(exc)
            raise  # raise since future is not done yet
        else:
            self.__step()


async def sleep(delay):
    future = Future()
    event_loop.loop.call_later(delay, future.set_result, None)
    return await future  # yield a empty future
