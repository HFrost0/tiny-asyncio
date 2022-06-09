import random
import time
from rich import print as rprint
import event_loop
from tasks import sleep


async def small_step():
    rprint('[red]small step')
    t1 = time.time()
    sleep_time = random.random()
    await sleep(sleep_time)
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


if __name__ == '__main__':
    loop = event_loop.loop
    loop.run_until_complete(main())
    print('Finished')
