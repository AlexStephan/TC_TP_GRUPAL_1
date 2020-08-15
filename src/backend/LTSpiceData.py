import ltspice
import numpy as np
from src.backend.dataFromFile import DataFromFile

class LTSpiceData(DataFromFile):
    def __init__(self):
        self.path = ""

    def isValid(self):
        if self.path.endswith('.raw'):
            return True
        else:
            return False

    def loadFile(self, path):
        self.path = path
        #print(self.path)
        l = ltspice.Ltspice(self.path)
        return l

    def getNames(self):
        sim = self.loadFile(self.path)
        sim.parse()
        names = sim.getVariableNames()
        names.pop(0)
        #print(names)
        return names

    def getGraph(self, name):
        print(name)
        sim = self.loadFile(self.path)
        sim.parse()
        freq = sim.getFrequency()
        var = sim.getData(name)
        var_amplitude = 20 * np.log10(np.abs(var))
        var_fase = np.angle(var, deg=True)
        return var_amplitude, var_fase
