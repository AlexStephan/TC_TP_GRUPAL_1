import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr


class TransferFunction:
    def __init__(self):
        self.w_arr = np.logspace(0,3,3000)
        self.t_arr = np.linspace(0,1000,1000) #en mseg

    def load_Hs(self,numerator,denominator):
        pass

    def set_linear_domain(self, min,max,num):
        self.t_arr = np.linspace(min,max,num)

    def set_log_domain(self, min,max,num):
        self.w = np.logspace(min,max,num)

    def is_valid(self):
        return True

    def get_bode(self): # tanto amplitud como fase, para hacer mas facil
        return [1,10,100,1000],[0,0,-3,-6],[0,0,45,90]

    def get_aproximated_bode(self): # porque confiamos en Tobi <3
        pass

    def get_Output(self,Input_Expression):
        pass

