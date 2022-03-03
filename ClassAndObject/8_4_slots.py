import sys
import logging

class Person:

    __slots__ = ["name","age","sex"]

    def __init__(self,name,age,sex):
        self.name = name
        self.age = age
        self.sex = sex

class Person2:


    def __init__(self,name,age,sex):
        self.name = name
        self.age = age
        self.sex = sex


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger('test')


    person = Person('yk',28,'男')
    person2 = Person2('yk',28,'男')

    log.debug("Person size %s"%sys.getsizeof(person))
    log.debug("Person2 size %s"%sys.getsizeof(person2))
