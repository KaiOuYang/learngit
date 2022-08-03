
import time
from queue import Queue
from threading import Thread

#简洁的线程间队列通信
def producer(out_q):
    while True:
        data = 1
        print("放入queue数据%s" % data)
        out_q.put(data)

def consumer(in_q):
    while True:
        data = in_q.get()
        print("从queue中拿取到数据%s"%data)

def test_originalPC():#简洁的线程间通信工具 queue使用。队列依然是线程安全的，因包含了必要的锁。
    q = Queue()
    t1 = Thread(target=producer,args=(q,))
    t2 = Thread(target=consumer,args=(q,))
    t1.start()
    t2.start()

#线程间队列通信增加停止功能
class ProducerCanStop:#相对于上面简洁的方式，此处增加了基于轮询的外部控制停止生产者producer、发送信号停止所有消费者consumer
    _sentinel = object()

    def __init__(self,out_q):
        self.running = True
        self.out_q = out_q

    def terminated(self):
        self.running =False

    def producer(self):
        data = 1
        while self.running:#可由terminated控制是否停止，停止后发送终止 消费者的信号
            self.out_q.put(data)
            data += 1
            time.sleep(1)
        self.out_q.put(ProducerCanStop._sentinel)

def consumerCanStop(in_q):
    while True:
        data = in_q.get()
        print("拿到数据%s"%data)
        if data is ProducerCanStop._sentinel:#读到该特殊值后又放回队列中，将之传递下去
            print("线程接收到停止信号...")
            in_q.put(ProducerCanStop._sentinel)#仍然放回去，使得监听该队列的线程链条上的线程们依次停止
            break

def test_advancePC():
    q = Queue()
    pInstance = ProducerCanStop(q)
    t1 = Thread(target=pInstance.producer)
    t2 = Thread(target=consumerCanStop,args=(q,))
    t1.start()
    t2.start()
    time.sleep(5)
    pInstance.terminated()

#自定义数据结构实现线程间通信
#通过创建自己的数据结构（比如创建优先级队列）并添加所需的锁和同步机制实现线程间通信

import heapq,threading

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._count = 0
        self._cv = threading.Condition()#相比event对象 具有锁，可线程安全

    def put(self,item,priority):
        with self._cv:
            heapq.heappush(self._queue,(-priority,self._count,item))
            self._count += 1
            self._cv.notify()

    def get(self):
        with self._cv:
            with len(self._queue) == 0:
                self._cv.wait()
            return heapq.heappop(self._queue)[-1]




if __name__ == '__main__':
    test_advancePC()