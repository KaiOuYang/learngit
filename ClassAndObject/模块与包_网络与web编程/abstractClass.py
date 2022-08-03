


from abc import ABCMeta,abstractmethod



class IStream(metaclass=ABCMeta):

    @abstractmethod
    def read(self,maxbytes=-1):
        pass

    @abstractmethod
    def write(self,data):
        pass


    @classmethod
    @abstractmethod
    def method1(cls):
        pass


class SocketStream(IStream):
    def read(self,maxbytes=-1):
        pass

    def write(self,data):
        pass


if __name__ == '__main__':

    s = SocketStream()