import time
from socket import socket
from threading import Thread

#Python 的线程更适用于处理 I/O 和其他需要并发执
#行的阻塞操作（比如等待 I/O、等待从数据库获取数据等等），而不是需要多处理器并
#行的计算密集型任务。
#线程是如何识别任务执行完毕然后自己退出呢？

def countdown(n):
    while n > 0:
        print('T-minus',n)
        n -= 1
        time.sleep(1)


class CountdownTask:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False
        print("结束该任务")

    def run(self,n):
        while self._running and n >0:
            print('T-minus',n)
            n -= 1
            time.sleep(1)


class IOTask:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False
        print("结束该任务")

    def run(self,sock):
        sock.settimeout(5)
        while self._running:
            try:
                data = sock.recv(8192)
                break
            except socket.timeout:
                continue
        #terminated
        return





if __name__ == '__main__':
    # t = Thread(target=countdown,args=(10,))#daemon=True则设置为后台线程，后台线程无法被等待即Join，将会在主线程终止时自动销毁
    # t.start()
    # t.join()#若加上join主线程将会等待t完成后再结束（即在此句阻塞等待），否则不会等待子线程
    # if t.is_alive():
    #     print("still running")
    # else:
    #     print("completed")
    # print("主线程结束...")

    #上述除了 start和join两个操作，没有其他可以对线程做的事情。比如结束线程，给它发送信号，调整它的调度以及其他高级操作。
    #若需要这些特性，需要自己添加！比如CountdownTask类就添加了终止线程的功能.是通过编程在发送给Thread的要执行的对象的
    # 某个特定点轮询某个与外部相关的信号来退出。但若线程执行些像I/O这样的阻塞操作，即在while循环体中被阻塞了，那通过轮询
    #来终止线程将会很麻烦，因无法返回。所以对于阻塞IO型任务得用超时机制来操作线程如 IOTask类，接受数据时若超时了则查询一遍
    #是否终止任务，若接到数据则开始处理数据

    c = CountdownTask()
    t = Thread(target=c.run,args=(10,))
    t.start()
    c.terminate()
    t.join()


