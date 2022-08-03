
from collections import deque


#之前都是以线程作为执行单元，若是替换成生成器，则有利有弊



#yield语句会让一个生成器挂起它的执行，所以再加一个调度器，将生成器当做某种"任务"并使用任务协作切换来替换
#它们的执行。TaskScheduler类在一个循环中运行生成器集合。
#若想使用生成器来实现简单的并发。就需要在实现actor或网络服务器的时候用生成器来替代线程。
def countdown(n):#生成器函数countdown，被调用后产生 生成器
    while n > 0:
        print('T-minus',n)
        yield
        n -= 1
    print('Blastoff!')

def countup(n):#生成器函数countup
    x = 0
    while x < n:
        print('Counting up',x)
        yield
        x += 1

class TaskScheduler:#任务调度器
    def __init__(self):
        self._task_queue = deque()

    def new_task(self,task):
        self._task_queue.append(task)

    def run(self):#将各个"任务"集中到集合中 循环协作切换
        while self._task_queue:
            task = self._task_queue.popleft()
            try:
                next(task)#向生成器发送信号，当生成器接收后将会执行到 yield后暂停退出并将控制权交还给  TaskScheduler.run
                self._task_queue.append(task)
            except StopIteration:
                pass



def test_taskScheduler():
    sched = TaskScheduler()
    sched.new_task(countdown(10))
    sched.new_task(countdown(5))
    sched.new_task(countup(15))
    sched.run()

if __name__ == '__main__':
    test_taskScheduler()