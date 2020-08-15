import numpy as np
import scipy.signal as ss

class TransferFunction:
    def __init__(self):

        self.valid = True

        self.numerator = []
        self.denominator = []
        self.HS = [] #transfer function
        self.poles = []
        self.zeros = []
        self.gain = 0;

        self.maxFreq = 0
        self.minFreq = 0
        self.numOfPoints = 0

        self.xAxis = []

        self.bode = []
        self.idealBode = []

    def load_Hs(self, numerator, denominator):
        if denominator == 0:
            valid = False
        else:
            self.numerator = numerator #guardo los coef del numerador
            self.denominator = denominator #guardo los coef del denominador
            self.gain = numerator[0]/denominator[0]

            self.HS = ss.TransferFunction(self.numerator, self.denominator) #armo la funcion transferencia
            self.poles = np.roots(denominator) #guardo los polos
            self.zeros = np.roots(numerator) #guardo los ceros

    def set_linear_domain(self, min, max, num): #armo un dominio lineal en el tiempo
        if min <= max:
            self.maxFreq = max
            self.minFreq = min
            self.numOfPoints = num
            self.xAxis = np.linspace(min, max, num)
        else:
            self.valid = False

    def set_log_domain(self, min, max, num): #armo un dominio logaritmico en el tiempo
        if min <= max:
            self.maxFreq = max
            self.minFreq = min
            self.numOfPoints = num
            self.xAxis = np.geomspace(min, max, num)
        else:
            self.valid = False

    def is_valid(self): #si algun dato que me enviaron fue invalido, aviso
        return self.valid

    def get_bode(self): # tanto amplitud como fase, para hacer mas facil
        self.bode = ss.bode(self.HS, self.xAxis)

    def get_aproximated_bode(self): # porque confiamos en Tobi <3// No confien pq es mas complicado de lo que pense xd
        pass