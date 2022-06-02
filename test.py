import time
from rich import print as rprint
import asyncio


# asyncio.sleep()

class Awaitable:
    def __init__(self, value):
        self.value = value

    def __await__(self):
        yield self

    __iter__ = __await__


async def small_step():
    rprint('[red]small step')
    await Awaitable((time.sleep, 1))
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
                pass
        else:
            raise Exception('task already done')


if __name__ == '__main__':
    # 主控
    t = Task(main())
    while True:
        t.run()
