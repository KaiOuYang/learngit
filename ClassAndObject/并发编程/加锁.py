

import threading
'''
1.标准锁 threading.Lock()
2.可重入锁 threading.RLock()
3.信号量同步模拟锁 Semaphore(5)
'''



class ShareCounter:
    #若是该类实例化出多个实例，则每个实例各自拥有自己的锁，相互独立
    def __init__(self,initial_value=0):
        self._value = initial_value
        self._value_lock = threading.Lock()#对该类的每一个实例中的可变对象加锁

    def incr(self,delta=1):
        with self._value_lock:
            self._value += delta

    def decr(self,delta=1):
        with self._value_lock:
            self._value -= delta

class ShareCounterClass:
    #该类的所有实例共享类级锁。
    #用于同步类方法，即该锁可以保证一次只有一个线程可以调用这个类方法。但该锁同时也是可重入锁，
    #所以与标准锁不同，即已经持有这个锁的方法在调用同样使用这个锁的方法时，无需再次获取锁。
    _lock = threading.RLock()
    def __init__(self,initial_value=0):
        self._value = initial_value

    def incr(self,delta=1):
        with ShareCounterClass._lock:
            self._value += delta

    def decr(self,delta=1):#可重入锁，此时调用incr 无需再次获取锁
        with ShareCounterClass._lock:
            self.incr(-delta)



from threading import Semaphore
import urllib.request
#使用信号量做线程同步，也是一种锁，限制一段代码的并发访问量。
_fetch_url_sema = Semaphore(5)
def fetch_url(url):
    with _fetch_url_sema:
        return urllib.request.urlopen(url)


if __name__ == '__main__':
    share = ShareCounter()
    share.incr()
    share.incr()
    share.incr()
    share.decr()
    print(share._value)
