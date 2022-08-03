import operator
import math

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point({!r:},{!r:})'.format(self.x,self.y)

    def distance(self,x,y):
        return math.hypot(self.x-x,self.y-y)



if __name__ == '__main__':

    points = [
        Point(10, -3),
        Point(1,2),
        Point(3,2),
        Point(3,0)

    ]
    #先形成一个可调用函数即 operator.methodcaller('distance',0,0)假定赋为d,
    #再将points中的每个元素经key对应的函数 d操作即d(element)，依据经该函数映射出来的结果对 原来的元素 进行排序
    #所以sort里面的key的意义在于将原始元素映射成衍生数据后，依据衍生数据对原来的元素进行排序。
    print(points.sort(key=operator.methodcaller('distance',0,0)))
    print(points)
