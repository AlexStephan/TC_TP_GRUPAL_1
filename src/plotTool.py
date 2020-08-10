# Imports

# Qt Modules
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from src.ui.tp1ui import Ui_Form

# Matplotlib Modules
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# Python Modules
import numpy as np
import scipy.signal as ss


class PlotTool(QWidget, Ui_Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("TP GRUPAL 1 - TEORÍA DE CIRCUITOS")

