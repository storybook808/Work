__author__ = 'Steven Chen'
__email__  = 'chenstev@hawaii.edu'

from math import sqrt

class List_Statistics(list):
    def __init__(self, *args):
        list.__init__(self, *args)

    
    def mean(self):
        return sum(self) / float(len(self))

    def std(self):
        result = List_Statistics()
        average = self.mean()
        for item in self:
            result.append(pow(item - average, 2))
        return sqrt(result.mean())