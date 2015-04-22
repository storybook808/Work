__author__ = 'Steven Chen'
__email__  = 'chenstev@hawaii.edu'

from collections import deque
from math import sqrt

class List_Statistics(deque):
    def __init__(self, *args):
        deque.__init__(self, *args)
        self.__sum__ = sum(self)
        self.__size__ = len(self)

    def pop(self):
        result = super(List_Statistics, self).popleft()
        self.__sum__ -= result
        self.__size__ -= 1
        return result

    def append(self, x):
        super(List_Statistics, self).append(x)
        self.__sum__ += x
        self.__size__ += 1
        return

    def mean(self):
        return (self.__sum__ / float(self.__size__))

    def std(self):
        result = List_Statistics()
        average = self.mean()
        for item in self:
            result.append(pow(item - average, 2))
        return sqrt(result.mean())

    def get_size(self):
        return self.__size__

    def get_sum(self):
        return self.__sum__