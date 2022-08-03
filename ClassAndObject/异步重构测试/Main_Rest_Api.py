
import pandas as pd
import os
import numpy as np
import time
import traceback
import sys
import logging
import openpyxl
import asyncio
from 异步重构测试 import common
from threading import Thread
import threading
from concurrent.futures import ThreadPoolExecutor
# module_logger = loggerCreate("MainModule.Main_Rest_Api")
# module_logger = logging.getLogger("MainModule.Main_Rest_Api")



class MainRestApi():
    '''
    添加新数据类型时，在Business_Factory.py中建立入口类,并在BusinessFactoryDict中增加映射
    '''


    @staticmethod
    async def Manage_Central(path, classLabel):
        if os.path.exists(path) is not True:
            # logger = logging.getLogger(__name__)
            print("该路径不存在!")
            return (('(8)','该路径不存在', path),)
        # print("进入Manage_Centra!")
        filepath_gen = MainRestApi.genFilePath(path)
        print("Manage_Central 函数 当前线程: %s"%threading.current_thread().name)
        df_filepath_gen = await MainRestApi.genDfAndFilePath(filepath_gen,classLabel)
        return df_filepath_gen

    @staticmethod
    def genFilePath(fileDirPath):
        if os.path.isfile(fileDirPath):
            print("文件路径: ", fileDirPath)
            yield  fileDirPath
        elif os.path.isdir(fileDirPath):
            print("文件夹路径: ", fileDirPath)
            for path, dirlist, filelist in os.walk(fileDirPath):
                for name in filelist:
                    filePath = os.path.join(path, name)
                    print(filePath)
                    yield filePath

    @staticmethod
    async def genDfAndFilePath(genPath, classLabel=None):
        # print("开始pd读取-----")
        for path_file in genPath:
            if path_file.endswith('.xlsx') or path_file.endswith('.xls'):
                t0 = time.time()
                print("****************%s 读取开始..." % path_file)
                writer = pd.ExcelWriter(path_file, engine='openpyxl')
                # Io_file = pd.io.excel.ExcelFile(path_file)  # dtype不能指定为str否则会把datetime类型的直接变为str,即后面接了很多0
                df = await MainRestApi.read_in_thread(writer)  # 输出一个字典，包含所有的sheet,指定格式object
                print("****************%s 读取完毕..."%path_file)
                elapsed = time.time() - t0
                print('读取时间花费: ',elapsed)
                return [df, path_file, writer]
                # yield df_dict, path_file, writer
                # del df_dict
            else:
                # logger = logging.getLogger(__name__)
                print(path_file, ' 不是xlsx格式的文件!')
                return []

    @staticmethod
    def genHandleDf(df, classLabel):#在此处收集异常信息组成字典
        result_return_list =[]
        return df
        # for df_dict,filepath,writer in df_dict_filepath_gen:#多个文件生成对应的多个df_dict
        #     return result_return_list

    @staticmethod
    async def read_in_thread(writer):#开线程来封装阻塞操作，
        #若这个函数并非是纯阻塞操作，即存在一些计算动作，则该函数会占用一些cpu的时间完成该计算后，后面的阻塞操作将释放GIL以及CPU由DMA代理，从而实现异步。
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None,MainRestApi.get_df,writer)
        return result


    @staticmethod
    def get_df(writer):
        df = pd.read_excel(writer, sheet_name=None, dtype=object)
        time.sleep(3)
        return df
