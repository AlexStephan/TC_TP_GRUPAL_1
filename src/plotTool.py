# Imports

from Lib.random import random

# Qt Modules
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFileDialog
from src.ui.tp1ui import Ui_Form

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

# My Own Modules

from src.backend.dataFromFile import DataFromFile


class Entrada(Enum):
    SUP = 0
    INF = 1
    BODE = 2


class Grafico(Enum):
    TEORICO = "."
    LTSPICE = "o"
    MEDIDO = "s"


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

        self.toolbarSuperior = NavigationToolbar(self.graficoSuperior_Canvas, self)
        self.toolbarInferior = NavigationToolbar(self.graficoInferior_Canvas, self) #Codigo Magico Gian
        self.navigation1.addWidget(self.toolbarSuperior)
        self.navigation2.addWidget(self.toolbarInferior)

        self.graficoSuperior_Axis = self.graficoSuperior_Figure.add_subplot()
        self.graficoInferior_Axis = self.graficoInferior_Figure.add_subplot()
        self.habilitarSegundoGrafico_CheckBox.stateChanged.connect(self.__cb_habilitarSegundoGrafico)
        self.__cb_habilitarSegundoGrafico()

        self.spice_PushButton.clicked.connect(self.__cb_spice)
        self.medicion_PushButton.clicked.connect(self.__cb_medido)

        self.borrarGraficos_PushButton.clicked.connect(self.__borrarGraficos)
        self.__borrarGraficos()

    def __add_plots(self, obj: DataFromFile,marker):
        size=obj.number_of_plots()

        if self.selectorGraficoEntrada_ComboBox.currentIndex() == Entrada.SUP.value:
            for index in range(size):
                x, y = obj.get_plot(index)
                self.__add_plot_superior(x, y,marker)
        elif self.selectorGraficoEntrada_ComboBox.currentIndex() == Entrada.INF.value:
            for index in range(size):
                x, y = obj.get_plot(index)
                self.__add_plot_inferior(x, y,marker)
        elif self.selectorGraficoEntrada_ComboBox.currentIndex() == Entrada.BODE.value:
            for index in range(size):
                x, y = obj.get_plot(index)
                if index % 2 == 0:
                    self.__add_plot_superior(x, y,marker)
                else:
                    self.__add_plot_inferior(x, y,marker)

    def __add_plot_superior(self,x,y,marker):
        self.graficoSuperior_Axis.plot(x,y, marker=marker)
        self.graficoSuperior_Canvas.draw()

    def __add_plot_inferior(self,x,y,marker):
        self.graficoInferior_Axis.plot(x,y, marker=marker)
        self.graficoInferior_Canvas.draw()

    def __cb_spice(self):
        path, _ = QFileDialog.getOpenFileName(filter="*.txt")

        data = DataFromFile()
        data.load_file(path)
        if data.is_valid():
            self.__add_plots(data,Grafico.LTSPICE.value)
        else:
            print("Archivo inválido")

    def __cb_medido(self):
        path, _ = QFileDialog.getOpenFileName(filter="*.csv")

        data = DataFromFile()
        data.load_file(path)
        if data.is_valid():
            self.__add_plots(data,Grafico.MEDIDO.value)
        else:
            print("Archivo inválido")

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
        self.selectorGraficoEntrada_ComboBox.setCurrentIndex(Entrada.SUP.value)

    def __borrarGraficos(self):
        self.graficoSuperior_Axis.clear()
        self.graficoSuperior_Axis.grid()
        self.graficoSuperior_Canvas.draw()

        self.graficoInferior_Axis.clear()
        self.graficoInferior_Axis.grid()
        self.graficoInferior_Canvas.draw()

