from . import futures
from . import events


class Task(futures.Future):
    def __init__(self, coro, loop=None):
        super().__init__(loop=loop)
        self._coro = coro
        self._loop.call_soon(self.__step)

    def __step(self, exc=None):
        if self.done():
            raise Exception('Task all ready done')
        try:
            if exc is None:
                result = self._coro.send(None)  # result is the future object yield from bottom
            else:
                result = self._coro.throw(exc)
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
            self.__step(exc)
        else:
            self.__step()


def gather(*coros_or_futures):
    loop = events.get_event_loop()
    if not coros_or_futures:
        outer = loop.create_future()
        outer.set_result([])
        return outer

    def _done_callback(fut):
        nonlocal nfinished
        nfinished += 1
        if nfinished == nfuts:
            results = []
            for c in children:
                results.append(c.result())
            outer.set_result(results)

    nfuts = 0
    nfinished = 0
    children = []
    for arg in coros_or_futures:
        fut = loop.create_task(arg)  # ensure future 🧐 fut is task actually
        nfuts += 1
        fut.add_done_callback(_done_callback)
        children.append(fut)
    outer = loop.create_future()
    return outer


async def sleep(delay):
    future = futures.Future()
    events.get_event_loop().call_later(delay, future.set_result, None)
    return await future  # yield a empty future
