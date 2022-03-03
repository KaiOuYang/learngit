import unittest
import random
import time
import numpy as np

from algrithom.binarySearch import ApplicationForBS
from algrithom.binarySearch import BinarySearch
import algrithom.commonConfig as common

class sortTest(unittest.TestCase):
    def setUp(self):
        self.lists = [2,3,4,4,4,7,7,8,9]
        self.lists2 = [2,3,4,7,8,9]
        self.target = 7


    def test_BinarySearch(self):
        result = ApplicationForBS.ipSearch(common.ips, '202.102.48.254')
        print(result)


    def test_binarySearchRightBorder(self):
        result = BinarySearch.binarySearchRightBorder(self.lists, self.target)
        print(result)

    def test_loopArrayBinarySearch(self):
        result = ApplicationForBS.loopArrayBinarySearch(self.lists2, self.target)
        print(result)

