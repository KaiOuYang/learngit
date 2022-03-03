import threading
import random
import time

resource = 0

semaphore = threading.Semaphore(1)

def increment():
    global resource
    semaphore.acquire()
    for i in range(10):
        print("执行线程1")
        resource += 1
        print(resource)
    semaphore.release()

def decrement():
    global resource
    semaphore.acquire()
    for i in range(10):
        print("执行线程2")
        resource -= 1
        print(resource)
    semaphore.release()

semaphore_tb = threading.Semaphore(0)
itemNumber = 0

def producer():
    global itemNumber
    itemNumber += 1
    print("生产资源: %s"%itemNumber)
    semaphore_tb.release()

def consumer():
    global itemNumber
    semaphore_tb.acquire()
    itemNumber -= 1
    print("获取资源: %s"%itemNumber)



if __name__ == '__main__':
    # incrementThread = threading.Thread(target=increment)
    # decrementThread = threading.Thread(target=decrement)
    # incrementThread.start()
    # decrementThread.start()
    # incrementThread.join()
    # decrementThread.join()

    producerThread = threading.Thread(target=producer)
    consumerThread = threading.Thread(target=consumer)
    consumerThread.start()
    producerThread.start()
    producerThread.join()
    consumerThread.join()