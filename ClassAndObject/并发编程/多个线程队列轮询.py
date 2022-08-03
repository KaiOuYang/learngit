
from multiprocessing import Process
import queue,socket,os
import select,threading


#轮询非文件类对象，比如队列，通常都是比较棘手的问题，若不适用套接字计数，那就只有用代码来循环
#遍历这些队列。但这样做不合理，会引入性能问题，比如若新的数据被加入到一个队列中，至少要花10毫秒
#才能被发现，若你之前的轮询还要去轮询其他对象，比如网络套接字那还会有更多问题。所以将队列与套接字
#等同，即用成对的套接字改造队列可以解决这些问题，一个单独的select调用可以同时用来轮询队列和网络
#套接字，没必要使用其他基于时间或周期性检查。甚至若数据被加入到一个队列，消费者集合可以实时被通知。
#只是会有些底层的I/O损耗。

#借助成对套接字的发送接收经由select轮询的触发机制作为事件消息到来的信号，队列底层由套接字监控，当有数据进入时本端套接字
# 将会给 对端套接字发送信息，此时处于队列中的对端套接字就有数据准备就绪，当用select轮询实现了fileno函数的队列时，当有
# 数据就绪的队列就会被拎出，然后用队列的get方法提取出消息

class PollableQueue(queue.Queue):#将队列与套接字等同对待
    def __init__(self):
        super().__init__()
        if os.name == 'posix':
            self._putsocket,self._getsocket = socket.socketpair()
        else:
            server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            server.bind(('127.0.0.1',0))
            server.listen(1)
            self._putsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self._putsocket.connect(server.getsockname())
            self._getsocket,_ = server.accept()
            server.close()

    def fileno(self):#使得该队列能被 select函数轮询
        return self._getsocket.fileno()

    def put(self,item):
        super().put(item)
        self._putsocket.send(b'x')

    def get(self):
        self._getsocket.recv(1)
        return super().get()

def consumer(queues):
    can_read,_,_ = select.select(queues,[],[])#队列实现了fileno函数，故是可被select轮询等待的
    for r in can_read:
        item = r.get()#拿出队列中的消息
        print('Got:',item)

def test_PollableQueue():
    q1 = PollableQueue()
    q2 = PollableQueue()
    q3 = PollableQueue()
    q1.put(1)
    q2.put(2)
    q3.put('2')
    q2.put(3)

    t = threading.Thread(target=consumer,args=([q1,q2,q3],))
    t.daemon = True
    t.start()


if __name__ == '__main__':#问题在于  主线程结束后子线程就结束了，所以拿不全所有的消息
    test_PollableQueue()



