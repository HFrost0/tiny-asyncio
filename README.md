# tiny-asyncio

A tiny python asyncio just for learning 🙋‍♂️, document below is my personal notes during the learning, may change
frequently.

## Event Loop

Event loop is just a `while True` loop, the basic functionality of event loop is to keep find out which functions can
be executed and execute them. Event loop's implementation I think is not related to coroutine or generator, it's just
a scheduler used to execute functions (even regardless their return value).

## Task and Future

The core code in `Future`

```python
def __await__(self):
    yield self


__iter__ = __await__
```

yield itself. and `Task`'s `__step` will receive bottom future object, and add done callback to them. Notice that
all function will be executed by a global event loop including `__step`. I think this part is the core part in asyncio.

## `yield from` and `await`

What eventually block the program in python design is the `yield`, while `yield from` (`await`) just keep send `None` to
generator (or we call coroutine) unless got a `StopIteration`, and

```python
x = yield from coro
```

`StopIteration`'s value will be assigned to x, notice that if we call `return` in generator or coroutine function
it will raise a `StopIteration`.

## Selectors

official python [selectors](https://docs.python.org/3/library/selectors.html) module

## todos

- [x] get_event_loop
- [x] selectors block
- [x] async sock connect
- [ ] async sock send
- [ ] async sock recv
- [ ] gather

## quote

* [cpython](https://github.com/python/cpython)

* [https://www.bilibili.com/video/BV1AB4y197k6](https://www.bilibili.com/video/BV1AB4y197k6)
