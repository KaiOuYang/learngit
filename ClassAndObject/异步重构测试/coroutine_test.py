
import time
import os,sys
import asyncio
from threading import Thread

now = lambda :time.time()
start = now()

async def do_some_work(x):
    print('开始执行: ',x)
    await asyncio.sleep(x)
    print("%s 已完成"%x)
    return x

def start_loop(loop):
    print("%s"%os.getpid())
    asyncio.set_event_loop(loop)
    loop.run_forever()

loop = asyncio.get_event_loop()
t = Thread(target=start_loop,args=(loop,))
t.start()
print('Time: ',now() - start)

asyncio.run_coroutine_threadsafe(do_some_work(3),loop)
asyncio.run_coroutine_threadsafe(do_some_work(6),loop)