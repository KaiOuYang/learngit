from collections import defaultdict
from contextlib import contextmanager
#引入一个单独的“交换机”或网关对象作为所有消息的中介。不直接将消息从一个任务发送到
#另一个，而是将其发送给交换机，然后由交换机将它发送给一个或多个被关联任务。

#通过队列发送消息的任务模式很普遍，但使用发布订阅模式的好处更明显。
#1.可简化大部分涉及到线程通信的工作，无需写通过多进程模块来操作多个线程，只需用交换机来连接它们，从而解耦多个任务Task
#2.带来全新的通信模式，可通过普通订阅者身份构建调试和诊断工具，即调试工具作为订阅者可拿到广播的消息从而做处理
#3.它能兼容多个"task-like"对象，可以是actor、协程、网络连接或任何正确实现了send()方法的东西

#注意点： 正确的绑定和解绑，每一个绑定者必须最终要解绑，类似于使用锁。故可以使用上下文管理器协议

#拓展：交换机可实现一整个消息通道集合或提供交换机名称的模式匹配规则，或扩展到分布式计算中，比如将消息路由到不同机器上面的任务中去。
class Exchange:

    def __init__(self):
        self._subscribers = set()#围绕一个集合，做增删改查

    def attach(self,task):
        self._subscribers.add(task)

    def detach(self,task):
        self._subscribers.remove(task)

    @contextmanager
    def subscribe(self,*tasks):
        for task in tasks:
            self.attach(task)
        try:
            yield #添加后跳出，即实例的_subscribers属性中添加了 task
        finally:
            for task in tasks:
                self.detach(task)

    def send(self,msg):
        for sub in self._subscribers:
            sub.send(msg)


_exchanges = defaultdict(Exchange)#存储所有已创建的 交换机


def get_exchange(name):#每个交换机通过一个名称定位
    return _exchanges[name]#一个交换机就是个普通对象，负责维护一个活跃的订阅者集合，并为绑定、解绑、发送消息提供相应的方法


class Task:
    def send(self,msg):
        print(msg)

def test_exchange():#消息被发送给一个交换机，交换机将它们发送给被绑定的订阅者 Task
    task_a = Task()
    task_b = Task()
    #用法1
    exc = get_exchange('name')
    exc.attach(task_a)
    exc.attach(task_b)
    exc.send('msg1')#给交换机发消息，交换机将发布到绑定的Task集合中
    exc.send('msg2')
    exc.detach(task_a)
    exc.detach(task_b)
    #用法2
    with exc.subscribe(task_a,task_b):
        exc.send('msg1')
        exc.send('msg2')

if __name__ == '__main__':
    test_exchange()