
from abc import ABCMeta,abstractmethod
from collections import Sequence

class IStream(metaclass=ABCMeta):

    @abstractmethod
    def read(self,maxbytes=-1):
        pass

    @abstractmethod
    def write(self,data):
        pass


class SocketStream(IStream):
    def read(self,maxbytes=-1):
        pass

    def write(self,data):
        pass


def parrot(voltage,state='a stiff',action='voom'):
    print(voltage,state,action)
    print(action)


if __name__ == '__main__':
    # i_stream = IStream()
    # IStream.register(Sequence)
    # s = Sequence()
    # if isinstance(s,IStream):
    #     print('yes')

    opts = {'voltage':1,'state':2,'action':3}
    parrot(opts)
