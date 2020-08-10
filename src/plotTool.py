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

        self.graficoSuperior_Figure = Figure()
        self.graficoInferior_Figure = Figure()
        self.graficoSuperior_Canvas = FigureCanvas(self.graficoSuperior_Figure)
        self.graficoInferior_Canvas = FigureCanvas(self.graficoInferior_Figure)
        self.graficoSuperior_Index = self.graficoSuperior_StackedWidget.addWidget(self.graficoSuperior_Canvas)
        self.graficoInferior_Index = self.graficoInferior_StackedWidget.addWidget(self.graficoInferior_Canvas)
        self.graficoSuperior_StackedWidget.setCurrentIndex(self.graficoSuperior_Index)
        self.graficoInferior_StackedWidget.setCurrentIndex(self.graficoInferior_Index)
        self.graficoSuperior_Axis = self.graficoSuperior_Figure.add_subplot()
        self.graficoInferior_Axis = self.graficoInferior_Figure.add_subplot()

        self.habilitarSegundoGrafico_CheckBox.stateChanged.connect(self.__cb_habilitarSegundoGrafico)
        self.__cb_habilitarSegundoGrafico()

    def __cb_habilitarSegundoGrafico(self):
        if self.habilitarSegundoGrafico_CheckBox.isChecked():
            self.__habilitarSegundoGrafico()
        else:
            self.__deshabilitarSegundoGrafico()

    def __habilitarSegundoGrafico(self):
        self.xLabel2_LineEdit.show()
        self.yLabel2_LineEdit.show()
        self.selectorGraficoEntrada_ComboBox.show()
        self.graficoInferior_StackedWidget.show()

    def __deshabilitarSegundoGrafico(self):
        self.xLabel2_LineEdit.hide()
        self.yLabel2_LineEdit.hide()
        self.selectorGraficoEntrada_ComboBox.hide()
        self.graficoInferior_StackedWidget.hide()

