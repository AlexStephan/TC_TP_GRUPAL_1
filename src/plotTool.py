# Imports

from Lib.random import random

# Qt Modules
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtWidgets, QtGui
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

# SymPy modules

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr

# My Own Modules

from src.backend.dataFromFile import DataFromFile
from src.backend.LTSpiceData import LTSpiceData
from src.backend.transferFunction import TransferFunction


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
        self.setWindowIcon(QtGui.QIcon('py.png'))

        self.LTSpice = LTSpiceData()
        self.ingresandoHs = False
        self.mostrarSp = False
        self.errorBox = QtWidgets.QMessageBox()

        self.Hs = TransferFunction()
        self.HsExpressionInstructions = "FUNCIONES EN FRECUENCIA COMPLEJA:\nVariable:\ts\n" \
                                        "Producto:\t*\nPotencia:\t**\nNo se admiten productos implícitos (ej: (2+s)(3+s))"

        self.graficoSuperior_Figure = Figure()
        self.graficoInferior_Figure = Figure()
        self.graficoSuperior_Canvas = FigureCanvas(self.graficoSuperior_Figure)
        self.graficoInferior_Canvas = FigureCanvas(self.graficoInferior_Figure)
        self.graficoSuperior_Index = self.graficoSuperior_StackedWidget.addWidget(self.graficoSuperior_Canvas)
        self.graficoInferior_Index = self.graficoInferior_StackedWidget.addWidget(self.graficoInferior_Canvas)
        self.graficoSuperior_StackedWidget.setCurrentIndex(self.graficoSuperior_Index)
        self.graficoInferior_StackedWidget.setCurrentIndex(self.graficoInferior_Index)

        self.toolbarSuperior = NavigationToolbar(self.graficoSuperior_Canvas, self)
        self.toolbarInferior = NavigationToolbar(self.graficoInferior_Canvas, self)  # Codigo Magico Gian
        self.navigation1.addWidget(self.toolbarSuperior)
        self.navigation2.addWidget(self.toolbarInferior)

        self.graficoSuperior_Axis = self.graficoSuperior_Figure.add_subplot()
        self.graficoInferior_Axis = self.graficoInferior_Figure.add_subplot()
        self.habilitarSegundoGrafico_CheckBox.stateChanged.connect(self.__cb_habilitarSegundoGrafico)
        self.__cb_habilitarSegundoGrafico()

        self.spice_PushButton.clicked.connect(self.__cb_spice)
        self.__habilita_deshabilita_Spice()
        self.spice_List.itemDoubleClicked.connect(self.__spice_Plot)

        self.medicion_PushButton.clicked.connect(self.__cb_medido)

        self.borrarGraficos_PushButton.clicked.connect(self.__borrarGraficos)
        self.__borrarGraficos()

        self.funcionTransferencia_PushButton.clicked.connect(self.__cb_Hs)
        self.__habilita_deshabilita_Hs()
        self.OK_Hs_PushButton.clicked.connect(self.__cb_Ok_Hs)

    def __error_message(self,description):
        self.errorBox.setWindowTitle("Error")
        self.errorBox.setIcon(self.errorBox.Information)
        self.errorBox.setText(description)
        self.errorBox.exec()

    def __add_plots_from_file(self,x, y, size,marker,legend):

        if self.selectorGraficoEntrada_ComboBox.currentIndex() == Entrada.SUP.value:
            for index in range(size):
                if size > 1:
                    yaux = y[index]
                else:
                    yaux = y
                self.__add_plot_superior(x, yaux,marker,legend)
        elif self.selectorGraficoEntrada_ComboBox.currentIndex() == Entrada.INF.value:
            for index in range(size):
                if size > 1:
                    yaux = y[index]
                else:
                    yaux = y
                self.__add_plot_inferior(x, yaux,marker,legend)
        elif self.selectorGraficoEntrada_ComboBox.currentIndex() == Entrada.BODE.value:
            for index in range(size):
                if size > 1:
                    yaux = y[index]
                else:
                    yaux = y
                if index % 2 == 0:
                    self.__add_plot_superior(x, yaux,marker,legend)
                else:
                    self.__add_plot_inferior(x, yaux,marker,legend)

    def __add_plot_superior(self,x,y,marker,legend):
        self.graficoSuperior_Axis.plot(x,y, marker=marker, label=legend)
        self.graficoSuperior_Canvas.draw()
        self.graficoSuperior_Axis.legend()

    def __add_plot_inferior(self,x,y,marker,legend):
        self.graficoInferior_Axis.plot(x,y, marker=marker, label=legend)
        self.graficoInferior_Canvas.draw()
        self.graficoInferior_Axis.legend()

    #Transferencia
    def __cb_Hs(self):
        self.ingresandoHs = not self.ingresandoHs
        self.__habilita_deshabilita_Hs()

    def __habilita_deshabilita_Hs(self):
        if self.ingresandoHs:
            self.__habilitarHs()
        else:
            self.__deshabilitarHs()

    def __habilitarHs(self):
        self.Numerador_LineEdit.show()
        self.Denominador_LineEdit.show()
        self.OK_Hs_PushButton.show()
        self.line_2.show()

        self.label_desde.show()
        self.label_hasta.show()
        self.label_pasos.show()
        self.spinBox_desde.show()
        self.spinBox_hasta.show()
        self.spinBox_pasos.show()

    def __deshabilitarHs(self):
        self.Numerador_LineEdit.hide()
        self.Denominador_LineEdit.hide()
        self.OK_Hs_PushButton.hide()
        self.line_2.hide()

        self.label_desde.hide()
        self.label_hasta.hide()
        self.label_pasos.hide()
        self.spinBox_desde.hide()
        self.spinBox_hasta.hide()
        self.spinBox_pasos.hide()

    def __cb_Ok_Hs(self):
        num = self.__parsing_Hs(self.Numerador_LineEdit.text(),"NUMERADOR")
        if num == []:
            return
        den = self.__parsing_Hs(self.Denominador_LineEdit.text(),"DENOMINADOR")
        if den == []:
            return

        self.Hs.load_Hs(num,den)
        self.Hs.set_log_domain(self.spinBox_desde.value(),
                               self.spinBox_hasta.value(),
                               self.spinBox_pasos.value())
        if self.Hs.is_valid():
            frecuencia,amplitud,fase=self.Hs.get_bode()
            # TODO: no llamar aca a las funciones de ploteo, sino mediante otra que distinga segun
            # el modo de grafico seleccionado (superior, inferior o "bode")
            self.__add_plot_superior(frecuencia,amplitud,Grafico.TEORICO.value,"TEORICO")
            self.__add_plot_inferior(frecuencia,fase,Grafico.TEORICO.value,"TEORICO")
        else:
            self.__error_message("No pudo calcularse la funcion de transferencia")



    def __parsing_Hs(self,string,description):
        s = sp.symbols('s')
        try:
            pol = parse_expr(string)
        except:
            self.__error_message("Se ingresó una expresión inválida en " + description + "\n\n"
                                 + self.HsExpressionInstructions)
            return []

        # print(pol.free_symbols)
        if pol.free_symbols == {s}:
            try:
                pol_coeff = pol.as_poly().all_coeffs()
            except:
                self.__error_message("La expresión ingresada en " + description + " no es un polinomio")
                return []
        elif pol.free_symbols == set():
            pol_coeff = []
            pol_coeff.append(pol.subs(s,0))
        else:
            self.__error_message(description + " no es una funcion monoevaluada en s")
            return []
        # print(pol_coeff)
        return pol_coeff

    #Spice
    def __cb_spice(self):
        path, _ = QFileDialog.getOpenFileName(filter="*.raw")
        self.LTSpice.loadFile(path)
        if self.LTSpice.isValid():
            self.spice_List.clear()
            if not self.mostrarSp:
                self.mostrarSp = not self.mostrarSp

            self.__habilita_deshabilita_Spice()
            self.spice_List.addItems(self.LTSpice.getNames())
        else:
            self.__error_message("Archivo Inválido")

    def __habilita_deshabilita_Spice(self):
        if self.mostrarSp:
            self.spice_List.show()
        else:
            self.spice_List.hide()

    def __spice_Plot(self):
        if  self.LTSpice.getMode() == 'AC':
            item = self.spice_List.currentItem().text()
            amp,phase,x = self.LTSpice.getGraph(item)
            y = [amp,  phase]
            self.__add_plots_from_file(x,y,2,Grafico.LTSPICE.value,"SIMULADO")

        elif self.LTSpice.getMode() == 'Transient':
            item = self.spice_List.currentItem().text()
            x, y = self.LTSpice.getGraph(item)
            self.__add_plots_from_file(x, y, 1, Grafico.LTSPICE.value, "SIMULADO")


    #Medicion
    def __cb_medido(self):
        path, _ = QFileDialog.getOpenFileName(filter="*.csv")

        data = DataFromFile()
        data.load_file(path)
        if data.is_valid():
            self.__add_plots_from_file(data,Grafico.MEDIDO.value,"MEDIDO")
        else:
            self.__error_message("Archivo Inválido")

    #Graficos

    def __cb_habilitarSegundoGrafico(self):
        if self.habilitarSegundoGrafico_CheckBox.isChecked():
            self.__habilitarSegundoGrafico()
        else:
            self.__deshabilitarSegundoGrafico()

    def __habilitarSegundoGrafico(self):
        #self.xLabel2_LineEdit.show()
        #self.yLabel2_LineEdit.show()
        self.selectorGraficoEntrada_ComboBox.show()
        self.graficoInferior_StackedWidget.show()
        self.frame_2.show()

    def __deshabilitarSegundoGrafico(self):
        #self.xLabel2_LineEdit.hide()
        #self.yLabel2_LineEdit.hide()
        self.selectorGraficoEntrada_ComboBox.hide()
        self.graficoInferior_StackedWidget.hide()
        self.frame_2.hide()
        self.selectorGraficoEntrada_ComboBox.setCurrentIndex(Entrada.SUP.value)

    def __borrarGraficos(self):
        self.graficoSuperior_Axis.clear()
        self.graficoSuperior_Axis.grid()
        self.graficoSuperior_Canvas.draw()

        self.graficoInferior_Axis.clear()
        self.graficoInferior_Axis.grid()
        self.graficoInferior_Canvas.draw()

