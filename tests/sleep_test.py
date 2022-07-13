import random
import time
from rich import print as rprint
import taio


async def small_step():
    rprint('[red]small step')
    t1 = time.time()
    sleep_time = random.random()
    await taio.sleep(sleep_time)
    assert time.time() - t1 > sleep_time
    rprint('[red]small step done')
    return sleep_time


async def big_step():
    rprint('[blue]big step')
    small_result = await small_step()
    rprint('[blue]big step done')
    return small_result


async def main():
    rprint('[green]main function run')
    big_result = await taio.gather(
        big_step(),
        big_step(),
        big_step()
    )
    rprint(f'[green]main function done {big_result}')
    return big_result


if __name__ == '__main__':
    loop = taio.get_event_loop()
    t = time.time()
    loop.run_until_complete(main())
    print(f'Finished {time.time() - t}')
