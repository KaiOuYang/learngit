

from queue import Queue
from threading import Thread,Event

# 一个actor就是一个并发执行的任务，只是简单的执行发送给它的消息任务。
#响应这些消息时，它可能还会给其他actor 发送更进一步的消息。actor 之间的通信是单向和异步的。因此，消息发送者不知
#道消息是什么时候被发送，也不会接收到一个消息已被处理的回应或通知。

#actor模式的魅力在于简单性，其实只有一个核心操作 send()。而在actor系统中的"消息"的泛化概念可用多种方式扩展
#比如以元组形式传递标签消息，让actor执行不同的操作(TaggedActor类)
#比如actor允许在一个工作者中运行任意的函数，并且通过一个特殊的Result对象返回结果
#最后，"发送"一个任务消息的概念可被扩展到多进程甚至是大型分布式系统中去，比如一个类actor对象的send方法可以被
#编程让它在一个套接字连接上传输数据或通过某些消息中间件(AMQP等)来发送。


class ActorExit(Exception):
    pass

class Actor:
    def __init__(self):
        self._mailbox = Queue()

    def send(self,msg):
        self._mailbox.put(msg)


    def recv(self):
        msg = self._mailbox.get()
        if msg is ActorExit:
            raise ActorExit()
        return msg

    def close(self):
        self.send(ActorExit)

    def start(self):
        self._terminated = Event()
        t = Thread(target=self._bootstrap)
        t.daemon = True
        t.start()

    def _bootstrap(self):
        try:
            self.run()
        except ActorExit:
            pass
        finally:
            self._terminated.set()

    def join(self):
        self._terminated.wait()

    def run(self):
        '''
        Run method to be implemented by the user
        :return:
        '''
        while True:
            msg = self.recv()


class PrintActor(Actor):
    '''
    使用actor实例（使用前实例要先start以启动后台线程）的send方法发送消息给它们。其机制是，这个方法会将消息放入一个队列_mailbox中，让后将其转交给
    处理被接受消息的一个内部线程(是经由start启动的将_bootstrap函数作为任务的后台线程,_bootstrap中将调用run函数后无限轮询recv，
    从队列_mailbox中取消息)
    '''

    def run(self):#run函数能被用户自定义其道理在于 用户可自定义接收的数据形式，并依据数据形式做自定义的业务内容
        while True:
            msg = self.recv()
            print('Got:',msg)


def test_PrintActor():
    p = PrintActor()
    p.start()
    p.send('HELL')
    p.send('work')
    p.close()
    p.join()

#以元组形式传递标签消息
class TaggedActor(Actor):
    def run(self):
        while True:
            tag,*payload = self.recv()#以元组形式传递标签消息，让actor执行不同的操作
            getattr(self,'do_'+tag)(*payload)

    def do_A(self,x):
        print('Running A',x)

    def do_B(self,x,y):
        print('Running B',x,y)

def test_taggedActor():
    a = TaggedActor()
    a.start()
    a.send(('A',1))
    a.send(('B',2,3))


#actor允许一个工作者中运行任意的函数，通过Result对象返回结果
#run函数会在start时就启动，等待队列中有元素，随后调用worker的submit提交任务与参数(本质是组合了send函数)，默认会带上用于
#监督结果的Result实例，此时队列中有元素，则run中的轮询数据接受到元素后，执行任务并将结果设置到Result对象中,
#因为没设置异步，所以当调用r.result()时会阻塞等待结果出来，则该线程就被卡住阻塞了。


class Worker(Actor):
    def submit(self,func,*args,**kwargs):# sumbit封装组合了 send
        r = Result()
        self.send((func,args,kwargs,r))#将用于监督结果的 Result实例作为参数辅助传入
        return r

    def run(self):
        while True:
            func,args,kwargs,r = self.recv()
            r.set_result(func(*args,**kwargs))#用Result对象来监控任务执行是否完成，若没完成则会阻塞


class Result:
    def __init__(self):
        self._evt = Event()
        self._result = None

    def set_result(self,value):
        self._result = value#若没计算出结果则会在此处阻塞
        self._evt.set()#通知已经计算出结果

    def result(self):
        self._evt.wait()#结果信号未明示，阻塞等待直到明示
        return self._result

def test_Worker():
    worker = Worker()
    worker.start()
    r = worker.submit('pow',2,3)#并行编程中进程池的submit工作机制应该是一样的
    print(r.result())

if __name__ == '__main__':
    test_PrintActor()