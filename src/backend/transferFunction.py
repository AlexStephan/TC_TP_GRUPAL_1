import numpy as np
import scipy.signal as ss
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr

class TransferFunction:
    def __init__(self):

        self.isFunctionValid = False
        self.isLinearValid = False
        self.isLogValid = False

        self.numerator = []
        self.denominator = []
        self.HS = [] #transfer function
        self.poles = []
        self.zeros = []
        self.gain = 0

        self.maxFreq = 0
        self.minFreq = 0
        self.numOfPoints = 0

        self.w_arr = []
        self.t_arr = []

        self.bode = []
        self.idealBode = []

    def load_Hs(self, numerator, denominator):
        if denominator == 0:
            self.isFunctionValid = False
        else:
            self.numerator = numerator #guardo los coef del numerador
            self.denominator = denominator #guardo los coef del denominador
            self.gain = numerator[0]/denominator[0]

            self.HS = ss.TransferFunction(self.numerator, self.denominator) #armo la funcion transferencia
            self.poles = np.roots(denominator) #guardo los polos
            self.zeros = np.roots(numerator) #guardo los ceros

            self.isFunctionValid = True

    def set_linear_domain(self, min, max, num): #armo un dominio lineal en el tiempo
        if min <= max:
            self.t_arr = np.linspace(min, max, num=num)
            self.isLinearValid = True
        else:
            self.isLinearValid = False

    def set_log_domain(self, min, max, num): #armo un dominio logaritmico en el tiempo
        if min <= max:
            self.maxFreq = 10**max
            self.minFreq = 10**min
            self.numOfPoints = num
            self.w_arr = np.logspace(min, max, num=num)
            self.w_arr = self.w_arr/(2*np.pi)
            self.isLogValid = True
        else:
            self.isLogValid = False

    def is_valid(self):  # si algun dato que me enviaron fue invalido, aviso
        return self.isLogValid and self.isLinearValid and self.isFunctionValid

    def get_bode(self):  # tanto amplitud como fase, para hacer mas facil
        self.bode = ss.bode(self.HS, self.w_arr)
        return self.bode[0]/2*np.pi,self.bode[1],self.bode[2]

    def get_aproximated_bode(self): # porque confiamos en Tobi <3// No confien pq es mas complicado de lo que pense xd
        pass

    def get_output(self, input_expression):
        if self.isLogValid and self.isLinearValid and self.isFunctionValid:
            return ss.lsim(self.HS, U=input_expression(self.t_arr),T=self.t_arr)
        else:
            return []
    def get_input(self, input_expression):
        if self.isLogValid and self.isLinearValid and self.isFunctionValid:
            return input_expression(self.t_arr)
        else:
            return []

