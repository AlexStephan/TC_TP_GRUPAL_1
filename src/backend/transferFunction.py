class TransferFunction:
    def __init__(self):
        pass

    def load_Hs(self,numerator,denominator):
        pass

    def set_linear_domain(self, min,max,num):
        pass

    def set_log_domain(self, min,max,num):
        pass

    def is_valid(self):
        return True

    def get_bode(self): # tanto amplitud como fase, para hacer mas facil
        return [1,10,100,1000],[0,0,-3,-6],[0,0,45,90]

    def get_aproximated_bode(self): # porque confiamos en Tobi <3
        pass