import os
import ltspice
import numpy as np
import matplotlib.pyplot as plt
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




l = ltspice.Ltspice(os.path.dirname(__file__)+'\IC_Charge-Discharge.raw')
# Make sure that the .raw file is located in the correct path
l.parse()

fig, axes = plt.subplots(1, 1, figsize=(20,7))

for i in range(l._case_num): # Iteration in simulation cases
    time = l.getTime(i)
    # Case number starts from zero
    # Each case has different time point numbers
    I_cap = l.getData('I(C)',i)
    #V_cap_max.append(max(V_cap))
    plt.plot(time, I_cap)

axes.set_xlabel("time [s]")
axes.set_ylabel("I(C) [A]")
plt.xlim((0, 150e-3))
plt.ylim((-0.8, 2.2))
plt.grid()
plt.savefig("IC_Charge_R_Equal_0.png")
plt.show()
