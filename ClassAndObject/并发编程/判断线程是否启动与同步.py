

from threading import Thread,Event
import time,threading


#线程的同步问题复杂，因线程的特性是每个线程都是独立运行且状态不可预测。若其他线程需要通过
#判断某个线程的状态来确定自己下一步操作，这就需要处理线程同步。可以用3种方式
#1.Event对象
    #该对象包含一个可由线程设置的信号标志，允许线程等待某些事件的发生。初始时，event对象中的信号标志为false，若有线程
    #等待该event对象，则该线程将会被阻塞直到该标志为true。当一个线程将这个event对象的信号标志设为真，它将唤醒全部等待
    #这个event对象的线程。
#2.semaphore信号量
    #因event被设置为真时会唤醒所有等待它的线程。若只是想唤醒单个线程呢？就用信号量semaphore或Condition对象替代，
    #在一个线程池中，每个线程都要获取到信号量，每次信号量被释放，只有一个线程会被唤醒并执行。
#3.Condition对象
    #因event对象最好一次性使用，很难确保安全的清理event对象并重新赋值，即一旦该event对象被设置为真就应该丢弃它。
    #若想重复的使用，则最好用Condition对象，因它能保证线程安全。且Condition对象也是会通知唤醒全部等待该对象的线程。

def countdown_event(n,started_evt):
    print("countdown starting")
    started_evt.set()#即将event对象设置为True，将会主动触发 全部 等待该event对象的线程
    while n > 0:
        print('T-minus',n)
        n -= 1
        time.sleep(1)

def test_countdown_event():
    started_evt = Event()
    print('Launching countdown')
    t = Thread(target=countdown_event,args=(10,started_evt))
    t.start()

    started_evt.wait()
    print('countdown is running')


def work_semaphore(n,sema):
    sema.acquire()
    print("working",n)

def work_release(sema):
    while True:
        print("release sema...")
        sema.release()
        time.sleep(1)

def test_work_semaphore():
    sema = threading.Semaphore(0)
    nworkers = 3
    r = threading.Thread(target=work_release,args=(sema,))
    r.start()
    for n in range(nworkers):#所有线程都在等待信号量能被持有，在终端或定时任务释放信号量seam.release()调试，否则什么都不会发生
        t = threading.Thread(target=work_semaphore,args=(n,sema,))
        t.start()

if __name__ == '__main__':
    a =None
    if a:
        print('不为空')