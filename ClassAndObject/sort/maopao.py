import random
import numpy as np
import time
import functools

def countTime(func):
    @functools.wraps(func)
    def calculate(*args,**kw):
        start_time = time.time()
        func(*args,**kw)
        end_time = time.time()
        elapsed = end_time - start_time
        print("%s spend time: %s"%(func.__name__,elapsed))
    return calculate

@countTime
def bubbleSort(lists):
    '''最原始的形式，哪怕数据已经有序也会进行比较'''
    length = len(lists)
    if length == 0:
        return
    for i in range(length):
        for j in range(length):
            if j >=length-1:
                break
            if lists[j] < lists[j+1]:
                lists[j],lists[j+1] = lists[j+1],lists[j]
    print(lists)
    return lists

@countTime
def bubbleSortOptimize1(lists):
    '''外部循环优化'''
    length = len(lists)
    if length == 0:
        return
    for i in range(length):
        flag = True
        for j in range(length):
            if j >=length-1:
                break
            if lists[j] < lists[j+1]:
                lists[j],lists[j+1] = lists[j+1],lists[j]
                flag = False#有数据移动则说明元素还未排好
        if flag:#当为True时，表明已无数据移动，元素已经排序好，不用继续循环
            break
    # print(lists)
    return lists

@countTime
def bubbleSortOptimize2(lists):
    '''外部循环+内部循环优化'''
    length = len(lists)
    if length == 0:
        return
    for i in range(length):
        flag = True
        for j in range(length):
            if j >=length-1-i:#每一次外部循环就已确定一个元素的位置，该确定的元素就不用加入计算
                break
            if lists[j] > lists[j+1]:
                lists[j],lists[j+1] = lists[j+1],lists[j]
                flag = False#有数据移动则说明元素还未排好
        if flag:#当为True时，表明已无数据移动，元素已经排序好，不用继续循环
            break
    print(lists)
    return lists

if __name__ == '__main__':
    listTest = np.random.randint(500,size=500)
    # bubbleSortOptimize1(listTest)
    bubbleSortOptimize2(listTest)
    # bubbleSort(listTest)
