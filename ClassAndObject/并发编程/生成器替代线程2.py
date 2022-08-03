
from collections import deque

#使用生成器实现一个不依赖线程的actor，此处的actor都是生成器

#ActorSchedule中的 new_actor与send函数作用都是往 队列 _msg_queue中填入消息，只不过new_actor是
#第一步收集(往队列填消息)即全收但不给信息，send则是选收(从第一步收集的中提取)即指定actor收集并给actor对应的信息
#run函数则就将 队列_msg_queue中的actor消息循环出来执行actor发送消息。
class ActorScheduler:

    def __init__(self):
        self._actors={}
        self._msg_queue = deque()#收集消息的队列


    def new_actor(self,name,actor):#往队列添加actor带None消息

        self._msg_queue.append((actor,None))
        self._actors[name] = actor

    def send(self,name,msg):#往队列添加指定name带msg的actor，即要让名为name的actor发送msg
        actor = self._actors.get(name)
        if actor:
            self._msg_queue.append((actor,msg))


    def run(self):
        while self._msg_queue:
            actor,msg = self._msg_queue.popleft()
            try:
                actor.send(msg)
            except StopIteration:
                pass

if __name__ == '__main__':
    def printer():
        while True:
            msg = yield
            print('Got: ',msg)

    def counter(sched):#计数生成器给自己发送消息并在sched中递归
        while True:
            n = yield
            if n == 0:
                break
            sched.send('printer',n)
            sched.send('counter',n-1)

    sched = ActorScheduler()
    sched.new_actor('printer',printer())
    sched.new_actor('counter',counter(sched))
    sched.send('counter',10000)
    sched.run()