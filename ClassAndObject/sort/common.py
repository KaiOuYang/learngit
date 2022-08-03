import time
import functools

def countTime(func):
    @functools.wraps(func)
    def calculate(*args,**kw):
        start_time = time.time()
        func(*args,**kw)
        end_time = time.time()
        elapsed = end_time - start_time
        print("%s spend time: %s"%(func.__name__,elapsed))
    return calculate