

from concurrent.futures import ProcessPoolExecutor
import time

#当将任务提交给子进程后，需要添加回调函数来非阻塞的等待结果。
# 回调函数接受一个Future实例，用来获取最终的结果，但要注意
#1.被提交的任务必须是简单函数形式，即def 语句定义的python函数。对于匿名方法、闭包、可调用实例和其他类型的并行执行还不支持
#2.函数参数和返回值必须兼容pickle，因为要使用到进程间的通信，所有解释器之间的交换数据必须被序列化
#3.被提交的任务不应该保留状态或有副作用，除了打印日志等简单的事
#4.混和使用进程池和多线程时，因创建任何线程前先创建并激活进程池(比如程序启动的main线程种创建进程池)
#5.要执行的任务量必须足够大以弥补额外的通信开销


def work(x):
    time.sleep(2)
    return 'done'


def test_parallel():

    with ProcessPoolExecutor() as pool:
        #2种方法提交,map与submit
        arg = 1
        future_result = pool.submit(work,arg)#submit手动单个提交
        r = future_result.result()

        datas = (1,1)
        results = pool.map(work,datas)#此处的results是一个迭代器，其中的每个元素都是work执行每个datas内的元素得到的结果