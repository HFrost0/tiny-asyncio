# TCP Echo Server

I implement a series of TCP echo servers for test.

### 1. select

Single thread (process) server with multiplexing `select` module.

### 2. selectors

Single thread (process) server with multiplexing `selectors` module which use `kqueue` or `epoll` according to OS.

### 3. selectors_process

Single process for listening new connection and multiple worker processes for response, each
process has multiplexing `selectors` module.

### 4. thread

Main thread for listening new connection. As long as there is a new connection, a new thread will be created for
response.

### 5. threadpool

Main thread for listening new connection, and a threadpool will be used to execute the response callbacks.

## Performances

Setup: all the results are obtained on macOS 12.4 M1 8 core chip laptop. selector_process server will have 4 worker
processes, and threadpool server will have a default `ThreadPoolExecutor` without worker number arg.

Tables blow shows the time spent (unit: second). For detail

* connect means the total connection time
* echo means the total send and recv time

connect + echo = total time consumed.

### 1k

1000 client connect and then each one send 100 times.

|         | select | selectors | selectors_process | thread  | threadpool |
|---------|--------|-----------|-------------------|---------|------------|
| connect | 0.2328 | 0.0427    | 0.0487            | 0.2784  | 0.0424     |
| echo    | 1.2135 | 1.2332    | 1.3918            | 24.4581 | 1.5212     |

### 10k

10,000 client connect and then each one send 100 times

|         | select | selectors | selectors_process | thread | threadpool |
|---------|--------|-----------|-------------------|--------|------------|
| connect | ❌      | 0.4142    | 0.4698            | ❌      | 0.4155     |
| echo    | ❌      | 16.2907   | 19.7788           | ❌      | 16.1532    |

❌ means failed the test, for the reason:

* select server failed because of the limit of maximum 1024 fd number of `select`.
* thread server failed because of too many thread created.

### 10k + cpu

10,000 client connect and then each one send 1 times, but server side is slow down by the cpu bound
task `sum(range(100000))`.

|         | select | selectors | selectors_process | thread | threadpool |
|---------|--------|-----------|-------------------|--------|------------|
| connect | ❌      | 0.7029    | 0.5843            | ❌      | 0.5510     |
| echo    | ❌      | 9.2716    | 2.9143            | ❌      | 9.9059     |

