from multiprocessing import Process, Pool
from 异步重构测试.Main_Rest_Api import MainRestApi
from tornado import gen
from tornado.httpserver import HTTPServer
import tornado.ioloop
import tornado.web
import json
import logging
import traceback
import sys
import os
from 异步重构测试 import common
import asyncio
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

import threading


# def start_loop(loop):
#     #将事件循环放到新开的子线程中运行避免堵塞主线程，经由全局变量将该事件传递
#     #到堵塞函数部分，在堵塞部分基于该事件循环开线程池来执行堵塞操作(解决第三方函数没有异步机制的问题)
#     # loop = asyncio.get_event_loop()
#     print("start_loop函数 当前线程: %s" % threading.current_thread().name)
#     asyncio.set_event_loop(loop)
#     common.new_loop = loop
#     loop.run_forever()



class Return_Data(tornado.web.RequestHandler):
    '''
    用于接收 各个标签的数据，进行数据清洗与治理
    '''

    async def get(self):
        print("Process (%s) is running..." % os.getpid())
        print("Return_Data.get() running!")
        path_files = self.get_argument("path")
        print("get path_files: %s in arguments" % path_files)
        class_label = self.get_argument("label")
        print("get class_label: %s in arguments" % class_label)
        # print("ClassLabel: ",ClassLabel)
        try:
            df_filepath_gen = await MainRestApi.Manage_Central(path_files, class_label)  # 由于目前只传入1个文件名，故set中只有一个tuple
            result = MainRestApi.genHandleDf(df_filepath_gen, class_label)
            # print("Return_Data.get() start to return infomation after all process! ")
            # print("已进入信息反馈阶段")
            if len(result) != 0:
                # for tuple_ele in result:  # Tuple_标识tuple包含了一个文件的处理结果
                #     tuple_item = [json.dumps(item) if type(item) is list else item for item in tuple_ele]
                #     return_status = '---'.join(tuple_item)
                #     # Mapping_status = dict_exception[Tuple_[0]]#不带状态信息,小胖那边会映射
                #     allstatus = '预处理' + return_status
                #     self.write(allstatus)
                self.write("读取成功 %s"%path_files)
            else:  # 可能该文件只存在一个空df
                temp_status = '预处理(1)---' + '空df---' + path_files
                self.write(temp_status)  # 需要改为更改的
        except:  # 未知错误
            print("exception occur in Tornado_Rest_Api.Return_Data.get()!")
            # print('Tornado_Rest_Api中报的运行异常')
            temp_status = '预处理(3)---' + 'Tornado部分时运行异常---' + path_files
            ex_type, ex_val, ex_stack = sys.exc_info()
            print("************************************************")
            print("ex_type: {}, ex_val: {}".format(ex_type, ex_val))
            for filename, linenum, funcname, source in traceback.extract_tb(ex_stack):
                print("%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname))
            self.write(temp_status)  # success 或者 error



def make_app():
    return tornado.web.Application(
        handlers=[
            (r'/', Return_Data),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "web/templates"),
        static_path=os.path.join(os.path.dirname(__file__), "web/static")
    )


if __name__ == "__main__":

    app = make_app()
    app.listen(8889, address="0.0.0.0")  # 8881,8883,8886
    print("listen to port 8889...")

    # http_server = HTTPServer(app)
    # http_server.bind(8889,address="0.0.0.0")
    # http_server.start(4)#开4个进程

    # common.new_loop = asyncio.new_event_loop()
    # t = Thread(target=start_loop,args=(common.new_loop,))#避免堵塞主线程循环
    # t.start()

    tornado.ioloop.IOLoop.current().start()