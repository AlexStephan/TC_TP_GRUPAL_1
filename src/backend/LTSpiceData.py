import ltspice
import numpy as np
from src.backend.dataFromFile import DataFromFile

class LTSpiceData(DataFromFile):
    def __init__(self):
        self.path = ""

    def loadFile(self, path):
        self.path = path
        print(self.path)
        l = ltspice.Ltspice(self.path)
        return l

    def getNames(self):
        sim = self.loadFile()
        sim.parse()
        names = sim.getVariableNames()
        return names

    def getGraph(self, name):
        sim = self.loadFile()
        sim.parse()
        freq = l.getFrequency()
        var = l.getData(name)
        var_amplitude = 20 * np.log10(np.abs(var))
        var_fase = np.angle(var, deg=True)
        return var_amplitude, var_fase
