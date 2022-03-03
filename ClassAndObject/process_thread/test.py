

from queue import Queue
from threading import Thread,Event

class ActorExit(Exception):
    pass

class Actor:
    '''
    一个actor即一个并发执行的任务，只简单的执行发送给它的消息任务。
    结合一个线程和一个队列即可定义actor
    '''
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
            self._terminated.wait()

    def join(self):
        self._terminated.wait()

    def run(self):
        while True:
            msg = self.recv()

class PrintActor(Actor):
    def run(self):
        while True:
            msg = self.recv()
            print('Got: ',msg)

if __name__ == '__main__':
    p = PrintActor()
    p.start()
    p.send('Hello')
    p.send('dd')
    p.close()
    p.join()