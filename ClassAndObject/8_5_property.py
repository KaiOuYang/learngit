import logging
import math

class Person:

    def __init__(self):
        self._name = '特性、非覆盖型描述符'
        self.__age = 1
        self.sex = None
        # self.name = None

    @property
    def name(self):
        return self._name

    # @name.setter
    # def name(self,val):
    #     if val >0:
    #         self._name =val
    #     else:
    #         raise ValueError("should be > 0")
    #
    # @name.deleter
    # def name(self):
    #     raise AttributeError("can't be delete")


class Circle:

    def __init__(self,radius):
        self.radius = radius

    @property
    def area(self):
        return math.pi * self.radius **2

    @property
    def diameter(self):
        return self.radius * 2

    @property
    def perimeter(self):
        return 2*math.pi*self.radius

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger('test')

    person = Person()
    person.name = 1
    log.debug("%s"%person.name)

    # cicle = Circle(3)
    # log.debug("%s"%cicle.area)
    # log.debug("%s"%cicle.diameter)
    # log.debug("%s"%cicle.perimeter)