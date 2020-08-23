# Imports
#

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
import array as arr

# SymPy modules

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr

# My Own Modules
from src.backend.CSVData import CSVData
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

        # PRIMER VENTANA

        self.LTSpice = LTSpiceData()
        self.CSV = CSVData()
        self.ingresandoHs = False
        self.mostrarSp = False
        self.errorBox = QtWidgets.QMessageBox()

        #Contadores
        self.numTeo = 0
        self.numMedi = 0
        self.numSimu = 0

        self.Hs = TransferFunction()
        self.HsExpressionInstructions = "FUNCIONES EN FRECUENCIA COMPLEJA:\nVariable:\ts\n" \
                                        "Producto:\t*\nPotencia:\t**\nNo se admiten productos implícitos (ej: (2+s)(3+s))"
        self.InExpressionInstructions = "FUNCIONES EN EL TIEMPO:\nVariable:\tt\n" \
                                        "Producto:\t*\nPotencia:\t**\nNo se admiten productos implícitos (ej: (2+t)(3+t))"
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
        self.PushButton_Cerrar_Spice.clicked.connect(self.__cb_cerrar_spice)
        self.__habilita_deshabilita_Spice()

        self.spice_List.itemDoubleClicked.connect(self.__spice_Plot)

        self.medicion_PushButton.clicked.connect(self.__cb_medido)

        self.borrarGraficos_PushButton.clicked.connect(self.__borrarGraficos)
        self.__borrarGraficos()
        self.refreshButton.clicked.connect(self.__cb_refresh)
        # self.__cb_refresh()

        self.funcionTransferencia_PushButton.clicked.connect(self.__cb_Hs)
        self.__habilita_deshabilita_Hs()
        self.OK_Hs_PushButton.clicked.connect(self.__cb_Ok_Hs)

        # SEGUNDA VENTANA
        self.aBode_Figure = Figure()
        self.aBode2_Figure = Figure()
        self.aIn_Figure = Figure()
        self.aOut_Figure = Figure()
        self.aPolosCeros_Figure = Figure()
        self.aBode_Canvas = FigureCanvas(self.aBode_Figure)
        self.aBode2_Canvas = FigureCanvas(self.aBode2_Figure)
        self.aIn_Canvas = FigureCanvas(self.aIn_Figure)
        self.aOut_Canvas = FigureCanvas(self.aOut_Figure)
        self.aPolosCeros_Canvas = FigureCanvas(self.aPolosCeros_Figure)
        self.aBode_Index = self.Analisis_Bode_stackedWidget.addWidget(self.aBode_Canvas)
        self.aBode2_Index = self.Analisis_Bode2_stackedWidget.addWidget(self.aBode2_Canvas)
        self.aIn_Index = self.Analisis_Entrada_stackedWidget.addWidget(self.aIn_Canvas)
        self.aOut_Index = self.Analisis_Salida_stackedWidget.addWidget(self.aOut_Canvas)
        self.aPolosCeros_Index = self.Analisis_PolosCeros_stackedWidget.addWidget(self.aPolosCeros_Canvas)
        self.Analisis_Bode_stackedWidget.setCurrentIndex(self.aBode_Index)
        self.Analisis_Bode2_stackedWidget.setCurrentIndex(self.aBode2_Index)
        self.Analisis_Entrada_stackedWidget.setCurrentIndex(self.aIn_Index)
        self.Analisis_Salida_stackedWidget.setCurrentIndex(self.aOut_Index)
        self.Analisis_PolosCeros_stackedWidget.setCurrentIndex(self.aPolosCeros_Index)

        self.aBode_toolvar = NavigationToolbar(self.aBode_Canvas, self)
        self.aBode2_toolvar = NavigationToolbar(self.aBode2_Canvas, self)
        self.aIn_toolvar = NavigationToolbar(self.aIn_Canvas, self)
        self.aOut_toolvar = NavigationToolbar(self.aOut_Canvas, self)
        self.aPolosCeros_toolvar = NavigationToolbar(self.aPolosCeros_Canvas,self)
        self.Analisis_Bode_navtool.addWidget(self.aBode_toolvar)
        self.Analisis_Bode2_navtool.addWidget(self.aBode2_toolvar)
        self.Analisis_Entrada_navtool.addWidget(self.aIn_toolvar)
        self.Analisis_Salida_navtool.addWidget(self.aOut_toolvar)
        self.Analisis_PolosCeros_navtool.addWidget(self.aPolosCeros_toolvar)

        self.aBode_Axis = self.aBode_Figure.add_subplot()
        self.aBode2_Axis = self.aBode2_Figure.add_subplot()
        self.aIn_Axis = self.aIn_Figure.add_subplot()
        self.aOut_Axis = self.aOut_Figure.add_subplot()
        self.aPolosCeros_Axis = self.aPolosCeros_Figure.add_subplot()

        self.Hs2 = TransferFunction()

        self.entrada_salida_separadas_checkBox.stateChanged.connect(self.__cb_checkear_entrada_salida_separados)
        self.__cb_checkear_entrada_salida_separados()
        self.__clean_Bode()
        self.__clean_PolosCeros()

        self.Analisis_Bode_Borrar.clicked.connect(self.__clean_Bode)
        self.Analisis_Entrada_Borrar.clicked.connect(self.__clean_In)
        self.Analisis_Salida_Borrar.clicked.connect(self.__clean_Out)
        self.Analisis_PolosCeros_Borrar.clicked.connect(self.__clean_PolosCeros)

        self.Analisis_Bode_Ok_pushButton.clicked.connect(self.__cb_analisis_ingreso_Bode)
        self.Analisis_Entrada_Ok_pushButton.clicked.connect(self.__cb_analisis_ingreso_entrada)
        self.Analisis_Salida_Ok_pushButton.clicked.connect(self.__cb_analisis_ingreso_salida)

    # SEGUNDA VENTANA

    #   Entradas y salidas juntas o separadas

    def __cb_checkear_entrada_salida_separados(self):
        if self.entrada_salida_separadas_checkBox.isChecked():
            self.__entrada_salida_separadas()
        else:
            self.__entrada_salida_juntas()

    def __entrada_salida_juntas(self):
        self.__clean_In()
        self.__clean_Out()

        self.frame_5.hide()
        self.Analisis_Salida_stackedWidget.hide()
        self.Analisis_Salida_Borrar.hide()
        self.Analisis_Salida_texto.hide()
        self.Analisis_Entrada_texto.hide()

    def __entrada_salida_separadas(self):
        self.__clean_In()
        self.__clean_Out()

        self.frame_5.show()
        self.Analisis_Salida_stackedWidget.show()
        self.Analisis_Salida_Borrar.show()
        self.Analisis_Salida_texto.show()
        self.Analisis_Entrada_texto.show()

    #   Limpieza graficos

    def __clean_Bode(self):
        self.aBode_Axis.clear()
        self.aBode_Axis.grid()
        self.aBode_Canvas.draw()

        self.aBode2_Axis.clear()
        self.aBode2_Axis.grid()
        self.aBode2_Canvas.draw()

    def __clean_In(self):
        self.aIn_Axis.clear()
        self.aIn_Axis.grid()
        self.aIn_Canvas.draw()

    def __clean_Out(self):
        self.aOut_Axis.clear()
        self.aOut_Axis.grid()
        self.aOut_Canvas.draw()

    def __clean_PolosCeros(self):
        self.aPolosCeros_Axis.clear()
        self.aPolosCeros_Axis.grid()
        self.aPolosCeros_Canvas.draw()

    # Ingreso del usuario

    def __cb_analisis_ingreso_Bode(self):

        #    num = self.__parsing_Hs(self.Analisis_Bode_Num_lineEdit.text(),"NUMERADOR")
        #    if num == []:
        #        return
        #    den = self.__parsing_Hs(self.Analisis_Bode_Den_lineEdit.text(),"DENOMINADOR")
        #    if den == []:
        #        return
        #
        #    self.Hs2.load_Hs(num,den)
        #    self.Hs2.set_log_domain(self.Analisis_Bode_Desde_spinBox.value(),
        #                           self.Analisis_Bode_Hasta_spinBox.value(),
        #                           self.Analisis_Bode_Pasos_spinBox.value())
        #    if self.Hs2.is_valid():
        #        frecuencia,amplitud,fase=self.Hs2.get_bode()
        #        # TODO: no llamar aca a las funciones de ploteo, sino mediante otra que distinga segun
        #        # el modo de grafico seleccionado (superior, inferior o "bode")
        #
        #        self.__add_Analisis_plot_Bode1(frecuencia,amplitud,Grafico.TEORICO.value,"TEORICO")
        #        self.__add_Analisis_plot_Bode2(frecuencia,fase,Grafico.TEORICO.value,"TEORICO")
        #    else:
        #        self.__error_message("No pudo calcularse la funcion de transferencia")
        #
        #    def __add_Analisis_plot_Bode1(self, x, y, marker, legend):
        #        self.aBode_Axis.plot(x, y, marker=marker)
        #        self.aBode_Canvas.draw()
        #        self.aBode_Axis.legend()

        num = self.__parsing_Hs(self.Analisis_Bode_Num_lineEdit.text(),"NUMERADOR")
        if num == []:
            return
        den = self.__parsing_Hs(self.Analisis_Bode_Den_lineEdit.text(),"DENOMINADOR")
        if den == []:
            return

        num_array = eval(num.__str__())
        den_array = eval(den.__str__())

        self.Hs2.load_Hs(num_array,den_array)

        self.Hs2.set_log_domain(self.Analisis_Bode_Desde_spinBox.value(),
                               self.Analisis_Bode_Hasta_spinBox.value(),
                               self.Analisis_Bode_Pasos_spinBox.value())
        self.Hs2.set_linear_domain(0,10,10)

        if self.Hs2.is_valid():
            frecuencia,amplitud,fase=self.Hs2.get_bode()
            polos=self.Hs2.get_polos()
            ceros=self.Hs2.get_ceros()

            xpolos = []
            ypolos = []
            for i in polos:
                xpolos.append(i.real)
                ypolos.append(i.imag)
            xceros = []
            yceros = []
            for i in ceros:
                xceros.append(i.real)
                yceros.append(i.imag)
            # y = [amplitud, fase]
            # self.__add_plots_from_file(frecuencia,y,2,Grafico.TEORICO.value,"TEORICO")
            self.__add_Analisis_plot_Bode1(frecuencia,amplitud,Grafico.TEORICO.value,"TEORICO")
            self.__add_Analisis_plot_Bode2(frecuencia, fase, Grafico.TEORICO.value, "TEORICO")
            self.__add_Analisis_plot_PolosCeros(xpolos,ypolos,'x',xceros,yceros,'o',"TEORICO")
        else:
            self.__error_message("No pudo calcularse la funcion de transferencia")

    def __parsing_ft(self, string, description):
        t = sp.symbols('t')
        try:
            expr = parse_expr(string)
        except:
            self.__error_message("Se ingresó una expresión inválida en " + description + "\n\n"
                                 + self.InExpressionInstructions)
            return None

        if expr.free_symbols == {t}:
            f_t = sp.lambdify(t,expr,modules=['numpy'])
        elif expr.free_symbols == set():
            f_t = np.vectorize(sp.lambdify(t,expr,modules=['numpy']))
        else:
            self.__error_message(description + " no es una funcion monoevaluada en t")
            return None
        return f_t

    def __add_Analisis_plot_Bode1(self, x, y, marker, legend):
        self.aBode_Axis.semilogx(x, y, marker=marker, label=legend)
        self.aBode_Axis.legend()
        self.aBode_Canvas.draw()

    def __add_Analisis_plot_Bode2(self, x, y, marker, legend):
        self.aBode2_Axis.semilogx(x, y, marker=marker, label=legend)
        self.aBode2_Axis.legend()
        self.aBode2_Canvas.draw()

    def __add_Analisis_plot_In(self,x,y,marker,legend):
        self.aIn_Axis.plot(x, y, marker=marker, label=legend)
        self.aIn_Axis.legend()
        self.aIn_Canvas.draw()

    def __add_Analisis_plot_Out(self,x,y,marker,legend):
        self.aOut_Axis.plot(x, y, marker=marker, label=legend)
        self.aOut_Axis.legend()
        self.aOut_Canvas.draw()

    def __add_Analisis_plot_PolosCeros(self,xpolos,ypolos,markerpolos,xceros,yceros,markerceros,legend):
        if xpolos != []:
            temp = self.aPolosCeros_Axis.scatter(xpolos,ypolos,marker=markerpolos,label=legend+' - Polos')
            color = temp.get_facecolor()[0]
            if xceros != []:
                self.aPolosCeros_Axis.scatter(xceros,yceros,marker=markerceros,label=legend+' - Ceros',color=color)
            self.aPolosCeros_Axis.legend()
        else:
            if xceros != []:
                self.aPolosCeros_Axis.scatter(xceros,yceros,marker=markerceros,label=legend+' - Ceros')
                self.aPolosCeros_Axis.legend()
        self.aPolosCeros_Canvas.draw()

    def __cb_analisis_ingreso_entrada(self):
        expr = self.__parsing_ft(self.Analisis_Bode_In_lineEdit.text(),"ENTRADA")
        if expr is None:
            return

        self.Hs2.set_linear_domain(0,
                                   self.Analisis_Entrada_Hasta_spinBox.value(),
                                   self.Analisis_Entrada_Pasos_spinBox.value())

        if not self.Hs2.is_valid():
            self.__error_message("Los parametros ingresados no son validos")
            return

        try:
            entrada = self.Hs2.get_input(expr)
            salida = self.Hs2.get_output(expr)
            if self.entrada_salida_separadas_checkBox.isChecked():
                self.__add_Analisis_plot_In(salida[0], entrada, Grafico.TEORICO.value, "TEORICO")
                self.__add_Analisis_plot_Out(salida[0], salida[1], Grafico.TEORICO.value, "TEORICO")
            else:
                self.__add_Analisis_plot_In(salida[0], entrada, Grafico.TEORICO.value, "ENTRADA")
                self.__add_Analisis_plot_In(salida[0], salida[1], Grafico.TEORICO.value, "RESPUESTA")
        except:
            self.__error_message("No pudo calcularse la respuesta del sistema")
            return

    def __cb_analisis_ingreso_salida(self):
        expr = self.__parsing_ft(self.Analisis_Bode_Out_lineEdit.text(),"SALIDA")
        if expr is None:
            return

        try:
            hasta = self.Analisis_Salida_Hasta_spinBox.value()
            pasos = self.Analisis_Salida_Pasos_spinBox.value()
            dominio = np.linspace(0,hasta,pasos)
            imagen = expr(dominio)
            if self.entrada_salida_separadas_checkBox.isChecked():
                self.__add_Analisis_plot_Out(dominio,imagen , Grafico.TEORICO.value, "ARBITRARIO")
            else:
                self.__add_Analisis_plot_In(dominio, imagen, Grafico.TEORICO.value, "ARBITRARIO")
        except:
            self.__error_message("No pudo graficarse la función arbitraria")
            return

    # PRIMERA VENTANA

    def __error_message(self, description):
        self.errorBox.setWindowTitle("Error")
        self.errorBox.setIcon(self.errorBox.Information)
        self.errorBox.setText(description)
        self.errorBox.exec()

    def __add_plots_from_file(self, x, y, size, marker, legend):

        if self.selectorGraficoEntrada_ComboBox.currentIndex() == Entrada.SUP.value:
            for index in range(size):
                if size > 1:
                    yaux = y[index]
                else:
                    yaux = y
                legend_ = legend + ' '*index
                self.__add_plot_superior(x, yaux, marker, legend_)
        elif self.selectorGraficoEntrada_ComboBox.currentIndex() == Entrada.INF.value:
            for index in range(size):
                if size > 1:
                    yaux = y[index]
                else:
                    yaux = y
                self.__add_plot_inferior(x, yaux, marker, legend)
        elif self.selectorGraficoEntrada_ComboBox.currentIndex() == Entrada.BODE.value:
            for index in range(size):
                if size > 1:
                    yaux = y[index]
                else:
                    yaux = y
                if index % 2 == 0:
                    self.__add_plot_superior(x, yaux, marker, legend)
                else:
                    self.__add_plot_inferior(x, yaux, marker, legend)


    def __add_plot_superior(self, x, y, marker, legend):
        self.graficoSuperior_Axis.semilogx(x, y, marker=marker, label=legend)
        self.graficoSuperior_Axis.legend()
        self.graficoSuperior_Canvas.draw()

    def __add_plot_inferior(self, x, y, marker, legend):
        self.graficoInferior_Axis.semilogx(x, y, marker=marker, label=legend)
        self.graficoInferior_Axis.legend()
        self.graficoInferior_Canvas.draw()

    # Transferencia
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
        num = self.__parsing_Hs(self.Numerador_LineEdit.text(), "NUMERADOR")
        if num == []:
            return
        den = self.__parsing_Hs(self.Denominador_LineEdit.text(), "DENOMINADOR")
        if den == []:
            return

        num_array = eval(num.__str__())
        den_array = eval(den.__str__())

        self.Hs.load_Hs(num_array, den_array)
        self.Hs.set_log_domain(self.spinBox_desde.value(),
                               self.spinBox_hasta.value(),
                               self.spinBox_pasos.value())
        self.Hs.set_linear_domain(0, 10, 10)
        if self.Hs.is_valid():
            frecuencia, amplitud, fase = self.Hs.get_bode()
            y = [amplitud, fase]
            self.__add_plots_from_file(frecuencia, y, 2, Grafico.TEORICO.value, "TEORICO "+self.numTeo.__str__())
            self.numTeo += 1
        else:
            self.__error_message("No pudo calcularse la funcion de transferencia")

    def __parsing_Hs(self, string, description):
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
            pol_coeff.append(pol.subs(s, 0))
        else:
            self.__error_message(description + " no es una funcion monoevaluada en s")
            return []
        # print(pol_coeff)
        return pol_coeff

    # Spice
    def __cb_spice(self):
        path, _ = QFileDialog.getOpenFileName(filter="*.raw")
        if path:
            self.LTSpice.loadFile(path)
        if self.LTSpice.isValid():
            self.spice_List.clear()
            if not self.mostrarSp:
                self.mostrarSp = not self.mostrarSp

            self.__habilita_deshabilita_Spice()
            self.spice_List.addItems(self.LTSpice.getNames())
        elif path:
            self.__error_message("Archivo Inválido")

    def __cb_cerrar_spice(self):
        self.mostrarSp = False
        self.__habilita_deshabilita_Spice()

    def __habilita_deshabilita_Spice(self):
        if self.mostrarSp:
            self.spice_List.show()
            self.PushButton_Cerrar_Spice.show()
        else:
            self.spice_List.hide()
            self.PushButton_Cerrar_Spice.hide()

    def __spice_Plot(self):
        if self.LTSpice.getMode() == 'AC':
            item = self.spice_List.currentItem().text()
            amp, phase, x = self.LTSpice.getGraph(item)
            y = [amp, phase]
            self.__add_plots_from_file(x, y, 2, Grafico.LTSPICE.value, "SIMULADO "+self.numSimu.__str__())
            self.numSimu += 1

        elif self.LTSpice.getMode() == 'Transient':
            item = self.spice_List.currentItem().text()
            x, y = self.LTSpice.getGraph(item)
            self.__add_plots_from_file(x, y, 1, Grafico.LTSPICE.value, "SIMULADO "+self.numSimu.__str__())
            self.numSimu += 1

    # Medicion
    def __cb_medido(self):
        path, _ = QFileDialog.getOpenFileName(filter="*.csv")
        if path:
            self.CSV.loadFile(path)
        if self.CSV.isValid():
            freq, amp, phase = self.CSV.getGraph()
            y = [amp, phase]
            self.__add_plots_from_file(freq, y, 2, Grafico.MEDIDO.value, "MEDIDO "+self.numMedi.__str__())
            self.numMedi += 1
        elif path:
            self.__error_message("Archivo Inválido")

    # Graficos
    def __cb_habilitarSegundoGrafico(self):
        if self.habilitarSegundoGrafico_CheckBox.isChecked():
            self.__habilitarSegundoGrafico()
        else:
            self.__deshabilitarSegundoGrafico()

    def __habilitarSegundoGrafico(self):
        # self.xLabel2_LineEdit.show()
        # self.yLabel2_LineEdit.show()
        self.selectorGraficoEntrada_ComboBox.show()
        self.graficoInferior_StackedWidget.show()
        self.frame_2.show()

    def __deshabilitarSegundoGrafico(self):
        # self.xLabel2_LineEdit.hide()
        # self.yLabel2_LineEdit.hide()
        self.selectorGraficoEntrada_ComboBox.hide()
        self.graficoInferior_StackedWidget.hide()
        self.frame_2.hide()
        self.selectorGraficoEntrada_ComboBox.setCurrentIndex(Entrada.SUP.value)

    def __cb_refresh(self):
        self.graficoSuperior_Axis.legend()
        self.graficoSuperior_Canvas.draw()
        self.graficoInferior_Axis.legend()
        self.graficoInferior_Canvas.draw()

    def __borrarGraficos(self):
        self.graficoSuperior_Axis.clear()
        self.graficoSuperior_Axis.grid()
        self.graficoSuperior_Canvas.draw()

        self.graficoInferior_Axis.clear()
        self.graficoInferior_Axis.grid()
        self.graficoInferior_Canvas.draw()

        self.numTeo = 0
        self.numMedi = 0
        self.numSimu = 0

