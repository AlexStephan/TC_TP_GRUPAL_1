import numpy as np
from Lib.random import random, randrange


class DataFromFile:
    def __init__(self):
        self.path = ""

    def load_file(self, path):
        self.path = path
        print(self.path)

    def is_valid(self):
        return self.path != ""

    def number_of_plots(self):
        return randrange(1,10,1)

    def get_plot(self,index):
        size = randrange(3,20,1)
        x = np.linspace(0,5,size)
        y = np.random.rand(size)
        return x,y

