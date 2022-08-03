

import threading
from contextlib import contextmanager

#尽可能保证每一个线程只能同时保持一个锁，这样程序就不会被死锁问题所困扰。一旦有线程同时申请多个锁，就不可预料了。
#避免死锁的2个常用方式:
#1.引入看门狗计数器。当线程正常运行时会每隔一段时间重置计数器，当未死锁时，一切正常运行。一旦发生死锁，则无法重置计数器
#   导致定时器超时，此时程序会通过重启自身恢复到正常状态。
#2. 获取锁时严格按照对象id升序排列获取，因不会产生循环依赖，即破解了死锁的必要条件


_local = threading.local()#可理解为全局 _local是一个字典，即该变量虽然是全局变量，但每个线程都只读自己线程的独立副本，互不干扰
# 它解决了参数在一个线程中各个函数之间互相传递的问题。

@contextmanager
def acquire(*locks):

    locks = sorted(locks,key=lambda x:id(x))#对锁升序排序

    acquired = getattr(_local,'acquired',[])#各个线程获取 _local.acquired都是各自线程的局部变量
    # 若线程独立空间中早已有 acquired属性 并且 已有属性中id最大值大于 传入的锁id，则报错
    #即该线程已经获取了一些锁，且这些锁并未按固定升序获取的则报错
    if acquired and max(id(lock) for lock in acquired) >= id(locks[0]):
        #之前获取的锁id应该要小于后来的。即后面进来的锁，id要更大，因是升序，若不符合则异常
        raise RuntimeError('Lock Order Violation')

    acquired.extend(locks)
    _local.acquired = acquired

    try:
        for lock in locks:#拿锁
            lock.acquire()
        yield#以此为分割点，上面部分为__enter__，下面为__exit__
    finally:
        for lock in reversed(locks):#释放锁，需要倒序释放,即先放id大的，再放小的
            lock.release()
        del acquired[-len(locks):]#倒数的方式 删除掉已经释放的锁


import threading,time


x_lock = threading.Lock()#锁1
y_lock = threading.Lock()#锁2

def thread_1():
    while True:
        with acquire(x_lock,y_lock):#无论获取多少锁，只要每个线程都按照固定顺序取锁放锁(除开嵌套锁)，则就可以保证不会出现死锁
            print("Thread-1")

def thread_2():
    while True:
        # time.sleep(1)
        with acquire(y_lock,x_lock):
            print("Thread-2")

#嵌套获取锁
def thread_1_nest():#嵌套锁中必然有一个线程会发生异常崩溃 RuntimeError: Lock Order Violation
    while True:
        with acquire(x_lock):
            with acquire(y_lock):
                print("Thread-1")

def thread_2_nest():
    while True:
        with acquire(y_lock):
            with acquire(x_lock):
                print("Thread-2")



#哲学家吃饭死锁问题，用固定顺序的锁可解

def philosopher(left,right):
    while True:
        with acquire(left,right):
            print(threading.current_thread(),'eating')

NSTICKS = 5
chopsticks = [threading.Lock() for n in range(NSTICKS)]


if __name__ == '__main__':
    t1 = threading.Thread(target=thread_1)
    t1.daemon =True
    # t1.start()
    # t1.join()

    t2 = threading.Thread(target=thread_2)
    # t2.daemon =True
    # t2.start()
    # t2.join()

    for n in range(NSTICKS):#哲学家吃饭加锁问题
        t = threading.Thread(target=philosopher,args=(chopsticks[n],chopsticks[(n+1)%NSTICKS]))
        t.start()



