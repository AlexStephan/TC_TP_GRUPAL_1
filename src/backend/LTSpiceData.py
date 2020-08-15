import ltspice
import numpy as np
from src.backend.dataFromFile import DataFromFile

class LTSpiceData(DataFromFile):
    def __init__(self):
        self.path = ""
        self.mode = ""

    def isValid(self):
        if self.path.endswith('.raw'):
            return True
        else:
            return False

    def loadFile(self, path):
        self.path = path
        #print(self.path)

    def getNames(self):
        sim = ltspice.Ltspice(self.path)
        sim.parse()
        self.mode = sim._mode
        names = sim.getVariableNames()
        names.pop(0)
        #print(names)
        return names

    def getGraph(self, name):
        #print(name)
        sim = ltspice.Ltspice(self.path)
        sim.parse()
        if self.mode == 'Transient':
            t = sim.getTime()
            var = sim.getData(name)
            return t, var

        elif self.mode == 'AC':
            freq = sim.getFrequency()
            var = sim.getData(name)
            var_amplitude = 20 * np.log10(np.abs(var))
            var_fase = np.angle(var, deg=True)
            return var_amplitude, var_fase, freq

    def getMode(self):
        return self.mode