from Lib.random import random



# Matplotlib Modules
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

# Python Modules
import numpy as np
import scipy.signal as ss
from enum import Enum

import sympy as sp
from sympy.polys.polytools import Poly

if __name__ == '__main__':
    try:
        num = sp.parsing.sympy_parser.parse_expr("(s+2)*(s+3)")
        print(num)

        s = sp.symbols('s')
        t = sp.symbols('t')
        print(num.subs(s, 4))
        lol = Poly(num, s)
        print(lol)

        hoh = s ** 2 + 5
        ha = sp.lambdify(s, hoh, modules=['numpy'])
        hoh.as_poly()
        try:
            print(num.as_poly().all_coeffs())
        except:
            print("d\'oh")
    except:
        print("otro d'oh")


