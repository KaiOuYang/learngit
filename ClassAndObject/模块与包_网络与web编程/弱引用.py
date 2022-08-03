


import weakref

class Node:

    def __init__(self,value):
        self.value = value
        self._parent = None
        self.children = []

    def __repr__(self):
        return 'Node({!r:})'.format(self.value)

    @property
    def parent(self):
        return None if self._parent is None else self._parent()#1此处若改为 self._parent

    @parent.setter
    def parent(self,node):
        self._parent = weakref.ref(node)#2此处若改为 node，则1和2综合作用，导致2个node循环相互引用，从而del不了


    def add_child(self,child):
        self.children.append(child)
        child.parent = self

#一旦出现循环引用，则python的垃圾回收机制基于简单的引用计数，无法解决该问题，所以有另外的垃圾回收器来专门针对循环引用，但关键
#不知道该机制什么时候会触发，尽管可以手动的gc.collect()触发它。就会出现内存泄露，所以使用弱引用来消除循环引用的问题，本质上，
#弱引用就是一个对象指针，不会增加它的引用计数，通过 weakref来创建弱引用，调用它即可


if __name__ == '__main__':
    root = Node("parent")
    c1 = Node("child")
    root.add_child(c1)
    print(c1.parent)
    del root
    print(c1.parent)