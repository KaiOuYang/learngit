import unittest
import random
import time
import numpy as np

from .linearSort import calculateSort
from .linearSort import baseNumSort


class sortTest(unittest.TestCase):
    def setUp(self):
        self.A = np.random.randint(1,10000,300000)
        # self.A = random.sample(range(1,100001),3000)
        # self.A = [1 ,2 ,1 ,0 ,4 ,3 ,6 ,7 ,5 ,8 ,9 ,4 ,6 ,7 ,8 ,8]
        self.B = np.random.randint(1,9,size=(1000,11))


    def test_baseNumSort(self):
        startTime = time.time()
        baseNumSort(self.B)
        elapsed = time.time() - startTime
        # print(result)
        print("基数排序花费时间: %s"%elapsed)

    def test_calculateSort(self):
        startTime = time.time()
        result = calculateSort(self.A)
        elapsed = time.time() - startTime
        # print(result)
        print("计数花费时间: %s"%elapsed)