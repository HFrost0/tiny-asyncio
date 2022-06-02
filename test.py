import random
import time
from rich import print as rprint
from event_loop import EventLoop


class Awaitable:
    def __init__(self, value):
        self.value = value

    def __await__(self):
        yield self

    __iter__ = __await__


async def small_step():
    rprint('[red]small step')
    t1 = time.time()
    sleep_time = random.random()
    await Awaitable(sleep_time)
    assert time.time() - t1 > sleep_time
    rprint('[red]small step done')
    return 1


async def big_step():
    rprint('[blue]big step')
    small_result = await small_step()
    rprint('[blue]big step done')
    return small_result * 10


async def main():
    rprint('[green]main function run')
    big_result = await big_step()
    rprint('[green]main function done')
    return big_result


class Task:
    def __init__(self, coro):
        self.coro = coro
        self._done = False
        self._result = None

    def run(self):
        if not self._done:
            try:
                x = self.coro.send(None)
                # x yield from 最里层
            except StopIteration as e:
                self._result = e.value
                self._done = True
            else:
                # receive block
                # func, arg = x.value  # 先不执行
                # func(arg)
                loop.call_later(x.value, self.run)
        else:
            raise Exception('task already done')


if __name__ == '__main__':
    t = Task(main())
    loop = EventLoop()
    loop.call_soon(t.run)
    loop.call_later(2.1, loop.stop)

    loop.run_forever()
