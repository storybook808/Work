__author__ = 'Steven Chen'
__email__  = 'chenstev@hawaii.edu'

from collections import deque
from list_statistics import List_Statistics

class Window:
    # Given : @sensor_id: A string of the sensor name for this window.
    # Return: Constructs a window object.
    def __init__(self, sensor_id):
        self.datetime = deque()
        self.sensor_id = sensor_id
        self.value = List_Statistics()

    # Given : @row: A list of three items that follows the format...
    #         [datetime, sensor id, value]
    # Return: A list of what was inserted into the data structure.
    def append(self, row):
        self.datetime.append(row[0])
        self.value.append(int(row[2]))
        return [self.datetime[-1], self.sensor_id, self.value[-1]]

    # Given : @index: A integer of the index the user wants to pop out.
    #         [datetime, sensor id, value]
    # Return: A list of what was popped from the data structure.
    def pop(self):
        return [self.datetime.popleft(), self.sensor_id, \
                self.value.pop()]

    # Given : Nothing.
    # Return: Average of the value lists in the form of a float.
    def average(self):
        return self.value.average()

    # Given : Nothing.
    # Return: Standard Deviation of the value lists in the form of a float.
    def std(self):
        return self.value.std()

    # Given : Nothing.
    # Return: Since the datetime and the value lists should contain the same
    #         count; we can just return the length of one of them.
    def size(self):
        return self.value.get_size()

    # Given : Nothing.
    # Return: Empties the data structure.
    def empty(self):
        self.datetime = deque()
        self.value = List_Statistics()

    # Given : Nothing.
    # Return: A string of what sensor this window is for.
    def who_am_i(self):
        return self.sensor_id

    # Given : Nothing.
    # Return: A string of the first datetime in the list.
    def startTime(self):
        return self.datetime[0]

    # Given : Nothing.
    # Return: A string of the last datetime in the list.
    def endTime(self):
        return self.datetime[-1]