from math import sqrt

class List_Statistics(list):
    def __init__(self, *args):
        list.__init__(self, *args)

    def mean(self):
        return sum(self) / float(len(self))

    def std(self):
        # Swap list.
        temp_list = List_Statistics()

        # Call the mean function once and store it to a variable.
        average = self.mean()

        for item in self:
            temp_list.append(pow(item - average, 2))

        return sqrt(temp_list.mean())