# Imports

# Qt Modules
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from src.ui.filtros import Ui_Form

# Matplotlib Modules
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# Python Modules
import numpy as np
import scipy.signal as ss

_PRIMER_ORDEN = 0
_SEGUNDO_ORDEN = 1

_PRIMER_ORDEN_PASA_BAJOS = 0
_PRIMER_ORDEN_PASA_ALTOS = 1
_PRIMER_ORDEN_PASA_TODO = 2
_PRIMER_ORDEN_ARBRITRARIO = 3
_PRIMER_ORDEN_INDETERMINADO = 4

_SEGUNDO_ORDEN_PASA_BAJOS = 0
_SEGUNDO_ORDEN_PASA_ALTOS = 1
_SEGUNDO_ORDEN_PASA_TODO = 2
_SEGUNDO_ORDEN_PASA_BANDA = 3
_SEGUNDO_ORDEN_NOTCH = 4
_SEGUNDO_ORDEN_LOWPASS_NOTCH = 5
_SEGUNDO_ORDEN_HIGHPASS_NOTCH = 6
_SEGUNDO_ORDEN_ARBITRARIO = 7
_SEGUNDO_ORDEN_INDETERMINADO = 8

#

_ENTRADA_SENOIDE = 0
_ENTRADA_ESCALON = 1
_ENTRADA_CUADRADA = 2


class MyWidget(QWidget, Ui_Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("TP FINAL ELECTOTECNIA")

        # Mis variables
        self.varGrado = _PRIMER_ORDEN
        self.varFiltro1er = _PRIMER_ORDEN_PASA_BAJOS
        self.varFiltro2do = _SEGUNDO_ORDEN_PASA_BAJOS
        self.varFiltroDeterminado = _PRIMER_ORDEN_PASA_BAJOS

        self.bodeMinimo = self.spinBodeMin.value()
        self.bodeMaximo = self.spinBodeMax.value()
        self.bodeTicks = self.spinBodeTicks.value()
        self.grafRtaTiempo = self.spinGrafRtaTiempo.value()*1e-3
        self.grafRtaTicks = self.spinGrafRtaTicks.value()

        self.varEntrada = _ENTRADA_SENOIDE
        self.varEntradaAmplitud = 0
        self.varEntradaFrecuencia = 0
        self.varEntradaFase = 0
        self.varEntradaPeriodo = 0
        self.varEntradaDutyCycle = 0

        self.varCero1 = 0 + 0j
        self.varCero2 = 0 + 0j
        self.varPolo1 = -5e-3 + 1j
        self.varPolo2 = -5e-3 - 1j

        # Para manejar mas facil algunos calculos...
        self.w_p = 0
        self.xi_p = 0
        self.w_z = 0
        self.xi_z = 0

        self.normalizingFactor = 1
        self.ganancia = 1
        self.isGananciaMaxima = 0

        self.w = np.logspace(self.bodeMinimo, self.bodeMaximo, self.bodeTicks)
        self.t = np.linspace(0, self.grafRtaTiempo, num=self.grafRtaTicks)
        self.numerator = [1, 1, 1]
        self.denominator = [1, -1, 1]
        self.H = ss.TransferFunction(self.numerator, self.denominator)
        self.h = ss.impulse(self.H, T=self.t)
        self.sinRta = ss.lsim(self.H, U=self.varEntradaAmplitud * np.cos(
            self.varEntradaFrecuencia * self.t + self.varEntradaFase * 2 * np.pi / 360), T=self.t)
        self.stepRta = ss.lsim(self.H, U=self.varEntradaAmplitud * np.heaviside(self.t, 1), T=self.t)
        self.sqrRta = ss.lsim(self.H, U=self.varEntradaAmplitud * (
                    self.t / self.varEntradaPeriodo - np.floor(self.t / self.varEntradaPeriodo) > (
                        1 - self.varEntradaDutyCycle / 100)), T=self.t)
        self.bode = ss.bode(self.H, self.w)
        self.rta = self.sinRta

        self.NULL_H = ss.TransferFunction([1], [1])

        # seteando figuras
        self.figureBode1 = Figure()
        self.figureBode2 = Figure()
        self.figurePolosCeros = Figure()
        self.figureRespuesta = Figure()

        self.canvasBode1 = FigureCanvas(self.figureBode1)
        self.canvasBode2 = FigureCanvas(self.figureBode2)
        self.canvasPolosCeros = FigureCanvas(self.figurePolosCeros)
        self.canvasRespuesta = FigureCanvas(self.figureRespuesta)

        self.canvasindexBode1 = self.stackedBodeAmplitud.addWidget(self.canvasBode1)
        self.canvasindexBode2 = self.stackedBodeFase.addWidget(self.canvasBode2)
        self.canvasindexPolosCeros = self.stackedPolosCeros.addWidget(self.canvasPolosCeros)
        self.canvasindexRespuesta = self.stackedWidget.addWidget(self.canvasRespuesta)

        self.stackedBodeAmplitud.setCurrentIndex(self.canvasindexBode1)
        self.stackedBodeFase.setCurrentIndex(self.canvasindexBode2)
        self.stackedPolosCeros.setCurrentIndex(self.canvasindexPolosCeros)
        self.stackedWidget.setCurrentIndex(self.canvasindexRespuesta)

        self.axisBode1 = self.figureBode1.add_subplot()
        self.axisBode2 = self.figureBode2.add_subplot()
        self.axisPolosCeros = self.figurePolosCeros.add_subplot()
        self.axisRespuesta = self.figureRespuesta.add_subplot()

        # seteando callbacks
        self.comboGrado.currentIndexChanged.connect(self.callback_combogrado)
        self.combo1er.currentIndexChanged.connect(self.callback_combo1er)
        self.combo2do.currentIndexChanged.connect(self.callback_combo2do)
        self.comboRespuesta.currentIndexChanged.connect(self.callback_comborta)
        self.pushSimular.clicked.connect(self.callback_pushsimular)

        # POLOS Y CEROS

        self.checkPolo_cero.stateChanged.connect(self.callback_checkpolo_cero)
        self.checkPolo_infinito.stateChanged.connect(self.callback_checkpolo_infinito)
        self.spinBoxPolo.valueChanged.connect(self.callback_spinpolo_cualquiera)
        self.spinBoxPoloIm.valueChanged.connect(self.callback_spinpolo_cualquiera)

        self.checkPolo_cero_2.stateChanged.connect(self.callback_checkpolo_cero_2)
        self.checkPolo_infinito_2.stateChanged.connect(self.callback_checkpolo_infinito_2)
        self.spinBoxPolo_2.valueChanged.connect(self.callback_spinpolo_cualquiera_2)
        self.spinBoxPoloIm_2.valueChanged.connect(self.callback_spinpolo_cualquiera_2)

        self.checkCero_cero.stateChanged.connect(self.callback_checkcero_cero)
        self.checkCero_infinito.stateChanged.connect(self.callback_checkcero_infinito)
        self.spinBoxCero.valueChanged.connect(self.callback_spincero_cualquiera)
        self.spinBoxCeroIm.valueChanged.connect(self.callback_spincero_cualquiera)

        self.checkCero_cero_2.stateChanged.connect(self.callback_checkcero_cero_2)
        self.checkCero_infinito_2.stateChanged.connect(self.callback_checkcero_infinito_2)
        self.spinBoxCero_2.valueChanged.connect(self.callback_spincero_cualquiera_2)
        self.spinBoxCeroIm_2.valueChanged.connect(self.callback_spincero_cualquiera_2)

        # GANANCIAS
        self.spinBoxGananciaBanda.valueChanged.connect(self.callback_ganancia)
        self.checkGananciaMaxima.stateChanged.connect(self.callback_ganancia)

        # FRECUENCIAS

        self.spinBoxFrecCorte.valueChanged.connect(self.callback_spinfrecuencias)
        self.spinBoxAmortiguamiento.valueChanged.connect(self.callback_spinfrecuencias)
        self.spinBoxFrecCorte_2.valueChanged.connect(self.callback_spinfrecuencias)
        self.spinBoxAmortiguamiento_2.valueChanged.connect(self.callback_spinfrecuencias)
        # ENTRADAS

        self.spinBoxRtaAmplitud.valueChanged.connect(self.callback_spinentrada)
        self.spinBoxRtaFrecuencia.valueChanged.connect(self.callback_spinentrada)
        self.spinBoxRtaFase.valueChanged.connect(self.callback_spinentrada)
        self.spinBoxRtaPeriodo.valueChanged.connect(self.callback_spinentrada)
        self.spinBoxRtaDuty.valueChanged.connect(self.callback_spinentrada)

        #

        self.spinBodeMin.valueChanged.connect(self.cambiandoDominioGraficos)
        self.spinBodeMax.valueChanged.connect(self.cambiandoDominioGraficos)
        self.spinBodeTicks.valueChanged.connect(self.cambiandoDominioGraficos)
        self.spinGrafRtaTicks.valueChanged.connect(self.cambiandoDominioGraficos)
        self.spinGrafRtaTiempo.valueChanged.connect(self.cambiandoDominioGraficos)

        self.callback_combogrado()
        self.callback_comborta()
        self.callback_spinentrada()
        self.callback_spinfrecuencias()
        self.callback_pushsimular()

        self.update_pictures()

    def cambiandoDominioGraficos(self):
        if self.spinBodeMax.value() <= self.spinBodeMin.value():
            self.spinBodeMax.setValue(self.spinBodeMin.value()+1)

        self.bodeMinimo = self.spinBodeMin.value()
        self.bodeMaximo = self.spinBodeMax.value()
        self.bodeTicks = self.spinBodeTicks.value()
        self.grafRtaTiempo = self.spinGrafRtaTiempo.value()*1e-3
        self.grafRtaTicks = self.spinGrafRtaTicks.value()

    def normalizando_h(self):
        if self.varGrado == _PRIMER_ORDEN:
            if self.varFiltroDeterminado == _PRIMER_ORDEN_PASA_BAJOS:
                self.normalizingFactor = -self.spinBoxPolo.value()
            elif self.varFiltroDeterminado == _PRIMER_ORDEN_PASA_ALTOS:
                self.normalizingFactor = 1
            elif self.varFiltroDeterminado == _PRIMER_ORDEN_PASA_TODO:
                self.normalizingFactor = 1
            else:
                self.normalizingFactor = 1
        else:
            local_cero1 = self.spinBoxCero.value() + 1j * self.spinBoxCeroIm.value()
            local_cero2 = self.spinBoxCero_2.value() + 1j * self.spinBoxCeroIm_2.value()
            local_polo1 = self.spinBoxPolo.value() + 1j * self.spinBoxPoloIm.value()
            local_polo2 = self.spinBoxPolo_2.value() + 1j * self.spinBoxPoloIm_2.value()

            local_wp = (np.sqrt(local_polo1 * local_polo2)).real
            if local_wp != 0:
                local_xip = ((local_polo1 + local_polo2) / (2 * local_wp)).real
            else:
                local_xip = 0

            local_wz = (np.sqrt(local_cero1 * local_cero2)).real
            if local_wz != 0:
                local_xiz = ((local_cero1 + local_cero2) / (2 * local_wz)).real
            else:
                local_xiz = 0

            if self.varFiltroDeterminado == _SEGUNDO_ORDEN_PASA_BAJOS:
                self.normalizingFactor = np.square(local_wp)
            elif self.varFiltroDeterminado == _SEGUNDO_ORDEN_PASA_ALTOS:
                self.normalizingFactor = 1
            elif self.varFiltroDeterminado == _SEGUNDO_ORDEN_PASA_TODO:
                self.normalizingFactor = 1
            elif self.varFiltroDeterminado == _SEGUNDO_ORDEN_PASA_BANDA:
                self.normalizingFactor = 2 * local_wp * local_xip
            elif self.varFiltroDeterminado == _SEGUNDO_ORDEN_NOTCH:
                self.normalizingFactor = 1
            elif self.varFiltroDeterminado == _SEGUNDO_ORDEN_LOWPASS_NOTCH:
                if local_wz != 0:
                    self.normalizingFactor = np.square(local_wp/local_wz)
                else:
                    self.normalizingFactor = 1
            elif self.varFiltroDeterminado == _SEGUNDO_ORDEN_HIGHPASS_NOTCH:
                self.normalizingFactor = 1
            else:
                self.normalizingFactor = 1

    def determining_filter(self):
        if self.varGrado == _PRIMER_ORDEN:
            if self.varFiltro1er == _PRIMER_ORDEN_ARBRITRARIO:
                # si el polo no es cero, pero es real, ta bien
                if self.checkPolo_cero.isChecked() == 0 and self.checkPolo_infinito.isChecked() == 0 and \
                        self.spinBoxPoloIm.value() == 0 and self.spinBoxPolo.value() != 0:
                    if self.checkCero_infinito.isChecked() == 1:
                        self.varFiltroDeterminado = _PRIMER_ORDEN_PASA_BAJOS
                    elif self.checkCero_cero.isChecked() == 1 or \
                            (
                                    self.spinBoxCero.value() == 0 and self.spinBoxCeroIm.value() == 0 and self.checkCero_infinito.isChecked() == 0):
                        self.varFiltroDeterminado = _PRIMER_ORDEN_PASA_ALTOS
                    elif self.spinBoxCeroIm.value() == 0 and self.spinBoxCero.value() == -self.spinBoxPolo.value():
                        self.varFiltroDeterminado = _PRIMER_ORDEN_PASA_TODO
                    else:
                        self.varFiltroDeterminado = _PRIMER_ORDEN_INDETERMINADO
                else:
                    self.varFiltroDeterminado = _PRIMER_ORDEN_INDETERMINADO

            else:
                self.varFiltroDeterminado = self.varFiltro1er
        else:
            if self.varFiltro2do == _SEGUNDO_ORDEN_ARBITRARIO:
                # POLOS DEL MISMO LADO DEL PLANO COMPLEJO, AMBOS REALES O COMPLEJOS CONJUGADOS
                # Ambos polos del mismo lado del plano complejo. No sobre el eje y
                if np.sign(self.spinBoxPolo.value()) == np.sign(self.spinBoxPolo_2.value()) and \
                        self.spinBoxPolo.value() != 0:

                    # Ambos polos reales, o complejos conjugados
                    if (self.spinBoxPoloIm.value() == 0 and self.spinBoxPoloIm_2.value() == 0) or \
                            (self.spinBoxPoloIm.value() == -self.spinBoxPoloIm_2.value() and
                             self.spinBoxPolo.value() == self.spinBoxPolo_2.value()):

                        if self.checkCero_infinito.isChecked() and self.checkCero_infinito_2.isChecked():
                            self.varFiltroDeterminado = _SEGUNDO_ORDEN_PASA_BAJOS
                        elif (self.checkCero_cero.isChecked() == 1 or
                              (
                                      self.spinBoxCero.value() == 0 and self.spinBoxCeroIm.value() == 0 and self.checkCero_infinito.isChecked() == 0)) and \
                                (self.checkCero_cero_2.isChecked() == 1 or
                                 (
                                         self.spinBoxCero_2.value() == 0 and self.spinBoxCeroIm_2.value() == 0 and self.checkCero_infinito_2.isChecked() == 0)):
                            self.varFiltroDeterminado = _SEGUNDO_ORDEN_PASA_ALTOS

                        elif (
                                self.spinBoxCero.value() == -self.spinBoxPolo.value() and self.spinBoxCeroIm.value() == self.spinBoxPoloIm.value() and
                                self.spinBoxCero_2.value() == -self.spinBoxPolo_2.value() and self.spinBoxCeroIm_2.value() == self.spinBoxPoloIm_2.value()) or \
                                (
                                        self.spinBoxCero.value() == -self.spinBoxPolo_2.value() and self.spinBoxCeroIm.value() == self.spinBoxPoloIm_2.value() and
                                        self.spinBoxCero_2.value() == -self.spinBoxPolo.value() and self.spinBoxCeroIm_2.value() == self.spinBoxPoloIm.value()):
                            self.varFiltroDeterminado = _SEGUNDO_ORDEN_PASA_TODO

                        elif ((self.checkCero_cero.isChecked() or (
                                self.spinBoxCero.value() == 0 and self.spinBoxCeroIm.value() == 0 and self.checkCero_infinito.isChecked() == 0)) and self.checkCero_infinito_2.isChecked()) or \
                                ((self.checkCero_cero_2.isChecked() or (
                                        self.spinBoxCero_2.value() == 0 and self.spinBoxCeroIm_2.value() == 0 and self.checkCero_infinito_2.isChecked() == 0)) and self.checkCero_infinito.isChecked()):
                            self.varFiltroDeterminado = _SEGUNDO_ORDEN_PASA_BANDA

                        else:

                            # si ambos ceros son reales (con mismo signo) o son complejos conjugados
                            if (self.spinBoxCeroIm.value() == 0 and self.spinBoxCeroIm_2.value() == 0 and
                                np.sign(self.spinBoxCero.value()) == np.sign(self.spinBoxCero_2.value())) or \
                                    (self.spinBoxCeroIm.value() == -self.spinBoxCeroIm_2.value() and
                                     self.spinBoxCero.value() == self.spinBoxCero_2.value()):

                                local_cero1 = self.spinBoxCero.value() + 1j * self.spinBoxCeroIm.value()
                                local_cero2 = self.spinBoxCero_2.value() + 1j * self.spinBoxCeroIm_2.value()
                                local_polo1 = self.spinBoxPolo.value() + 1j * self.spinBoxPoloIm.value()
                                local_polo2 = self.spinBoxPolo_2.value() + 1j * self.spinBoxPoloIm_2.value()

                                local_wp = (np.sqrt(local_polo1 * local_polo2)).real
                                local_xip = ((local_polo1 + local_polo2) / (2 * local_wp)).real

                                local_wz = (np.sqrt(local_cero1 * local_cero2)).real
                                local_xiz = ((local_cero1 + local_cero2) / (2 * local_wz)).real

                                if local_wp < local_wz:
                                    self.varFiltroDeterminado = _SEGUNDO_ORDEN_LOWPASS_NOTCH
                                elif local_wp > local_wz:
                                    self.varFiltroDeterminado = _SEGUNDO_ORDEN_HIGHPASS_NOTCH
                                else:
                                    self.varFiltroDeterminado = _SEGUNDO_ORDEN_NOTCH

                            else:
                                self.varFiltroDeterminado = _SEGUNDO_ORDEN_INDETERMINADO
                    else:
                        self.varFiltroDeterminado = _SEGUNDO_ORDEN_INDETERMINADO
                else:
                    self.varFiltroDeterminado = _SEGUNDO_ORDEN_INDETERMINADO
            else:
                self.varFiltroDeterminado = self.varFiltro2do

    def renaming_filter(self):
        if self.varGrado == _PRIMER_ORDEN:
            if self.varFiltroDeterminado == _PRIMER_ORDEN_PASA_BAJOS:
                self.labelTipoFiltro.setText('Filtro primer orden: PASA BAJOS')
            elif self.varFiltroDeterminado == _PRIMER_ORDEN_PASA_ALTOS:
                self.labelTipoFiltro.setText('Filtro primer orden: PASA ALTOS')
            elif self.varFiltroDeterminado == _PRIMER_ORDEN_PASA_TODO:
                self.labelTipoFiltro.setText('Filtro primer orden: PASA TODO')
            else:
                self.labelTipoFiltro.setText('Filtro primer orden: INDETERMINADO')
        else:
            if self.varFiltroDeterminado == _SEGUNDO_ORDEN_PASA_BAJOS:
                self.labelTipoFiltro.setText('Filtro segundo orden: PASA BAJOS')
            elif self.varFiltroDeterminado == _SEGUNDO_ORDEN_PASA_ALTOS:
                self.labelTipoFiltro.setText('Filtro segundo orden: PASA ALTOS')
            elif self.varFiltroDeterminado == _SEGUNDO_ORDEN_PASA_BANDA:
                self.labelTipoFiltro.setText('Filtro segundo orden: PASA BANDA')
            elif self.varFiltroDeterminado == _SEGUNDO_ORDEN_PASA_TODO:
                self.labelTipoFiltro.setText('Filtro segundo orden: PASA TODO')
            elif self.varFiltroDeterminado == _SEGUNDO_ORDEN_NOTCH:
                self.labelTipoFiltro.setText('Filtro segundo orden: NOTCH')
            elif self.varFiltroDeterminado == _SEGUNDO_ORDEN_LOWPASS_NOTCH:
                self.labelTipoFiltro.setText('Filtro segundo orden: LOW-PASS NOTCH')
            elif self.varFiltroDeterminado == _SEGUNDO_ORDEN_HIGHPASS_NOTCH:
                self.labelTipoFiltro.setText('Filtro segundo orden: HIGH-PASS NOTCH')
            else:
                self.labelTipoFiltro.setText('Filtro segundo orden: INDETERMINADO')

    def read_ceros_polos(self):
        if self.checkPolo_cero.isChecked():
            self.varPolo1 = 0 + 0j
        elif self.checkPolo_infinito.isChecked():
            self.varPolo1 = float('inf')
        else:
            self.varPolo1 = self.spinBoxPolo.value() + 1j * self.spinBoxPoloIm.value()

        if self.checkPolo_cero_2.isChecked():
            self.varPolo2 = 0 + 0j
        elif self.checkPolo_infinito_2.isChecked():
            self.varPolo2 = float('inf')
        else:
            self.varPolo2 = self.spinBoxPolo_2.value() + 1j * self.spinBoxPoloIm_2.value()

        if self.checkCero_cero.isChecked():
            self.varCero1 = 0 + 0j
        elif self.checkCero_infinito.isChecked():
            self.varCero1 = float('inf')
        else:
            self.varCero1 = self.spinBoxCero.value() + 1j * self.spinBoxCeroIm.value()

        if self.checkCero_cero_2.isChecked():
            self.varCero2 = 0 + 0j
        elif self.checkCero_infinito_2.isChecked():
            self.varCero2 = float('inf')
        else:
            self.varCero2 = self.spinBoxCero_2.value() + 1j * self.spinBoxCeroIm_2.value()

    # EDICION ENTRADA MEDIANTE GUI

    def callback_spinentrada(self):
        self.varEntradaAmplitud = self.spinBoxRtaAmplitud.value()
        self.varEntradaFrecuencia = self.spinBoxRtaFrecuencia.value()
        self.varEntradaFase = self.spinBoxRtaFase.value()
        self.varEntradaPeriodo = self.spinBoxRtaPeriodo.value() * 1e-3
        self.varEntradaDutyCycle = self.spinBoxRtaDuty.value()

    # EDICION FRECUENCIAS MEDIANTE GUI

    def callback_spinfrecuencias(self):
        if self.varGrado == _PRIMER_ORDEN:
            if self.varFiltro1er == _PRIMER_ORDEN_PASA_BAJOS:
                self.checkCero_infinito.setChecked(1)
                self.spinBoxPolo.setValue(-self.spinBoxFrecCorte.value())
                self.spinBoxPoloIm.setValue(0)
            elif self.varFiltro1er == _PRIMER_ORDEN_PASA_ALTOS:
                self.checkCero_cero.setChecked(1)
                self.spinBoxPolo.setValue(-self.spinBoxFrecCorte.value())
                self.spinBoxPoloIm.setValue(0)
            elif self.varFiltro1er == _PRIMER_ORDEN_PASA_TODO:
                self.spinBoxCero.setValue(self.spinBoxFrecCorte.value())
                self.spinBoxCeroIm.setValue(0)
                self.spinBoxPolo.setValue(-self.spinBoxFrecCorte.value())
                self.spinBoxPoloIm.setValue(0)
            else:
                self.spinBoxPolo.setValue(-self.spinBoxFrecCorte.value())
                self.spinBoxPoloIm.setValue(0)
        else:
            if self.varFiltro2do == _SEGUNDO_ORDEN_LOWPASS_NOTCH:
                if self.spinBoxFrecCorte_2.value() < self.spinBoxFrecCorte.value():
                    self.spinBoxFrecCorte_2.setValue(self.spinBoxFrecCorte.value())
            if self.varFiltro2do == _SEGUNDO_ORDEN_HIGHPASS_NOTCH:
                if self.spinBoxFrecCorte_2.value() > self.spinBoxFrecCorte.value():
                    self.spinBoxFrecCorte_2.setValue(self.spinBoxFrecCorte.value())

            self.w_p = complex(self.spinBoxFrecCorte.value())
            self.xi_p = complex(self.spinBoxAmortiguamiento.value())
            self.w_z = complex(self.spinBoxFrecCorte_2.value())
            self.xi_z = complex(self.spinBoxAmortiguamiento_2.value())

            if self.varFiltro2do == _SEGUNDO_ORDEN_PASA_BAJOS:
                self.checkCero_infinito.setChecked(1)
                self.checkCero_infinito_2.setChecked(1)
                self.spinBoxPolo.setValue((self.w_p * (-self.xi_p + np.sqrt(np.square(self.xi_p) - 1))).real)
                self.spinBoxPoloIm.setValue((self.w_p * (-self.xi_p + np.sqrt(np.square(self.xi_p) - 1))).imag)
                self.spinBoxPolo_2.setValue((self.w_p * (-self.xi_p - np.sqrt(np.square(self.xi_p) - 1))).real)
                self.spinBoxPoloIm_2.setValue((self.w_p * (-self.xi_p - np.sqrt(np.square(self.xi_p) - 1))).imag)
            elif self.varFiltro2do == _SEGUNDO_ORDEN_PASA_ALTOS:
                self.checkCero_cero.setChecked(1)
                self.checkCero_cero_2.setChecked(1)
                self.spinBoxPolo.setValue((self.w_p * (-self.xi_p + np.sqrt(np.square(self.xi_p) - 1))).real)
                self.spinBoxPoloIm.setValue((self.w_p * (-self.xi_p + np.sqrt(np.square(self.xi_p) - 1))).imag)
                self.spinBoxPolo_2.setValue((self.w_p * (-self.xi_p - np.sqrt(np.square(self.xi_p) - 1))).real)
                self.spinBoxPoloIm_2.setValue((self.w_p * (-self.xi_p - np.sqrt(np.square(self.xi_p) - 1))).imag)
            elif self.varFiltro2do == _SEGUNDO_ORDEN_PASA_TODO:
                self.spinBoxCero.setValue((-self.w_p * (-self.xi_p + np.sqrt(np.square(self.xi_p) - 1))).real)
                self.spinBoxCeroIm.setValue((-self.w_p * (-self.xi_p + np.sqrt(np.square(self.xi_p) - 1))).imag)
                self.spinBoxCero_2.setValue((-self.w_p * (-self.xi_p - np.sqrt(np.square(self.xi_p) - 1))).real)
                self.spinBoxCeroIm_2.setValue((-self.w_p * (-self.xi_p - np.sqrt(np.square(self.xi_p) - 1))).imag)

                self.spinBoxPolo.setValue((self.w_p * (-self.xi_p + np.sqrt(np.square(self.xi_p) - 1))).real)
                self.spinBoxPoloIm.setValue((self.w_p * (-self.xi_p + np.sqrt(np.square(self.xi_p) - 1))).imag)
                self.spinBoxPolo_2.setValue((self.w_p * (-self.xi_p - np.sqrt(np.square(self.xi_p) - 1))).real)
                self.spinBoxPoloIm_2.setValue((self.w_p * (-self.xi_p - np.sqrt(np.square(self.xi_p) - 1))).imag)
            elif self.varFiltro2do == _SEGUNDO_ORDEN_PASA_BANDA:
                self.checkCero_cero.setChecked(1)
                self.checkCero_infinito_2.setChecked(1)
                self.spinBoxPolo.setValue((self.w_p * (-self.xi_p + np.sqrt(np.square(self.xi_p) - 1))).real)
                self.spinBoxPoloIm.setValue((self.w_p * (-self.xi_p + np.sqrt(np.square(self.xi_p) - 1))).imag)
                self.spinBoxPolo_2.setValue((self.w_p * (-self.xi_p - np.sqrt(np.square(self.xi_p) - 1))).real)
                self.spinBoxPoloIm_2.setValue((self.w_p * (-self.xi_p - np.sqrt(np.square(self.xi_p) - 1))).imag)
            elif self.varFiltro2do == _SEGUNDO_ORDEN_NOTCH:
                self.spinBoxCero.setValue(0)
                self.spinBoxCeroIm.setValue(self.w_p.real)
                self.spinBoxCero_2.setValue(0)
                self.spinBoxCeroIm_2.setValue(-self.w_p.real)

                self.spinBoxPolo.setValue((self.w_p * (-self.xi_p + np.sqrt(np.square(self.xi_p) - 1))).real)
                self.spinBoxPoloIm.setValue((self.w_p * (-self.xi_p + np.sqrt(np.square(self.xi_p) - 1))).imag)
                self.spinBoxPolo_2.setValue((self.w_p * (-self.xi_p - np.sqrt(np.square(self.xi_p) - 1))).real)
                self.spinBoxPoloIm_2.setValue((self.w_p * (-self.xi_p - np.sqrt(np.square(self.xi_p) - 1))).imag)
            else:
                self.spinBoxCero.setValue((self.w_z * (-self.xi_z + np.sqrt(np.square(self.xi_z) - 1))).real)
                self.spinBoxCeroIm.setValue((self.w_z * (-self.xi_z + np.sqrt(np.square(self.xi_z) - 1))).imag)
                self.spinBoxCero_2.setValue((self.w_z * (-self.xi_z - np.sqrt(np.square(self.xi_z) - 1))).real)
                self.spinBoxCeroIm_2.setValue((self.w_z * (-self.xi_z - np.sqrt(np.square(self.xi_z) - 1))).imag)

                self.spinBoxPolo.setValue((self.w_p * (-self.xi_p + np.sqrt(np.square(self.xi_p) - 1))).real)
                self.spinBoxPoloIm.setValue((self.w_p * (-self.xi_p + np.sqrt(np.square(self.xi_p) - 1))).imag)
                self.spinBoxPolo_2.setValue((self.w_p * (-self.xi_p - np.sqrt(np.square(self.xi_p) - 1))).real)
                self.spinBoxPoloIm_2.setValue((self.w_p * (-self.xi_p - np.sqrt(np.square(self.xi_p) - 1))).imag)

    # EDICION DE POLOS Y CEROS MEDIANTE GUI

    def callback_ganancia(self):
        self.ganancia = self.spinBoxGananciaBanda.value()
        self.isGananciaMaxima = self.checkGananciaMaxima.isChecked()

    def callback_checkpolo_cero(self):
        if self.checkPolo_cero.isChecked():
            self.checkPolo_infinito.setChecked(0)
            self.spinBoxPolo.setValue(0)
            self.spinBoxPoloIm.setValue(0)
        self.read_ceros_polos()

    def callback_checkpolo_cero_2(self):
        if self.checkPolo_cero_2.isChecked():
            self.checkPolo_infinito_2.setChecked(0)
            self.spinBoxPolo_2.setValue(0)
            self.spinBoxPoloIm_2.setValue(0)
        self.read_ceros_polos()

    def callback_checkcero_cero(self):
        if self.checkCero_cero.isChecked():
            self.checkCero_infinito.setChecked(0)
            self.spinBoxCero.setValue(0)
            self.spinBoxCeroIm.setValue(0)
        self.read_ceros_polos()

    def callback_checkcero_cero_2(self):
        if self.checkCero_cero_2.isChecked():
            self.checkCero_infinito_2.setChecked(0)
            self.spinBoxCero_2.setValue(0)
            self.spinBoxCeroIm_2.setValue(0)
        self.read_ceros_polos()

    def callback_checkpolo_infinito(self):
        if self.checkPolo_infinito.isChecked():
            self.checkPolo_cero.setChecked(0)
        self.read_ceros_polos()

    def callback_checkpolo_infinito_2(self):
        if self.checkPolo_infinito_2.isChecked():
            self.checkPolo_cero_2.setChecked(0)
        self.read_ceros_polos()

    def callback_checkcero_infinito(self):
        if self.checkCero_infinito.isChecked():
            self.checkCero_cero.setChecked(0)
        self.read_ceros_polos()

    def callback_checkcero_infinito_2(self):
        if self.checkCero_infinito_2.isChecked():
            self.checkCero_cero_2.setChecked(0)
        self.read_ceros_polos()

    def callback_spinpolo_cualquiera(self):
        self.checkPolo_cero.setChecked(0)
        self.checkPolo_infinito.setChecked(0)
        self.read_ceros_polos()

    def callback_spinpolo_cualquiera_2(self):
        self.checkPolo_cero_2.setChecked(0)
        self.checkPolo_infinito_2.setChecked(0)
        self.read_ceros_polos()

    def callback_spincero_cualquiera(self):
        self.checkCero_cero.setChecked(0)
        self.checkCero_infinito.setChecked(0)
        self.read_ceros_polos()

    def callback_spincero_cualquiera_2(self):
        self.checkCero_cero_2.setChecked(0)
        self.checkCero_infinito_2.setChecked(0)
        self.read_ceros_polos()

    # EDICION GRADOS MEDIANTE GUI

    def callback_combogrado(self):
        if self.comboGrado.currentIndex() == 0:
            self.varGrado = _PRIMER_ORDEN
        else:
            self.varGrado = _SEGUNDO_ORDEN
        self.update_grado_config_window()
        if self.varGrado == _PRIMER_ORDEN:
            self.update_grado1_config_window()
        else:
            self.update_grado2_config_window()

    def callback_combo1er(self):
        if self.combo1er.currentIndex() == 0:
            self.varFiltro1er = _PRIMER_ORDEN_PASA_BAJOS
            self.checkCero_infinito.setChecked(1)
            self.spinBoxPolo.setValue(-1)
            self.spinBoxPoloIm.setValue(0)
        elif self.combo1er.currentIndex() == 1:
            self.varFiltro1er = _PRIMER_ORDEN_PASA_ALTOS
            self.checkCero_cero.setChecked(1)
            self.spinBoxPolo.setValue(-1)
            self.spinBoxPoloIm.setValue(0)
        elif self.combo1er.currentIndex() == 2:
            self.varFiltro1er = _PRIMER_ORDEN_PASA_TODO
            self.spinBoxPolo.setValue(-1)
            self.spinBoxPoloIm.setValue(0)
            self.spinBoxCero.setValue(1)
            self.spinBoxCeroIm.setValue(0)
        else:
            self.varFiltro1er = _PRIMER_ORDEN_ARBRITRARIO
        self.update_grado1_config_window()
        self.callback_spinfrecuencias()

    def callback_combo2do(self):
        if self.combo2do.currentIndex() == 0:
            self.varFiltro2do = _SEGUNDO_ORDEN_PASA_BAJOS
        elif self.combo2do.currentIndex() == 1:
            self.varFiltro2do = _SEGUNDO_ORDEN_PASA_ALTOS
        elif self.combo2do.currentIndex() == 2:
            self.varFiltro2do = _SEGUNDO_ORDEN_PASA_TODO
        elif self.combo2do.currentIndex() == 3:
            self.varFiltro2do = _SEGUNDO_ORDEN_PASA_BANDA
        elif self.combo2do.currentIndex() == 4:
            self.varFiltro2do = _SEGUNDO_ORDEN_NOTCH
        elif self.combo2do.currentIndex() == 5:
            self.varFiltro2do = _SEGUNDO_ORDEN_LOWPASS_NOTCH
        elif self.combo2do.currentIndex() == 6:
            self.varFiltro2do = _SEGUNDO_ORDEN_HIGHPASS_NOTCH
        else:
            self.varFiltro2do = _SEGUNDO_ORDEN_ARBITRARIO
        self.update_grado2_config_window()
        self.callback_spinfrecuencias()

    def callback_comborta(self):
        if self.comboRespuesta.currentIndex() == 0:
            self.varEntrada = _ENTRADA_SENOIDE
        elif self.comboRespuesta.currentIndex() == 1:
            self.varEntrada = _ENTRADA_ESCALON
        else:
            self.varEntrada = _ENTRADA_CUADRADA
        self.update_entrada_config_window()

    def callback_pushsimular(self):
        self.w = np.logspace(self.bodeMinimo, self.bodeMaximo, self.bodeTicks)
        self.t = np.linspace(0, self.grafRtaTiempo, num=self.grafRtaTicks)

        self.determining_filter()
        self.normalizando_h()
        # defining H (grado 2)
        if self.varGrado == _PRIMER_ORDEN:
            if self.varCero1 != float('inf'):
                self.numerator = [1, -self.varCero1]
            else:
                self.numerator = [1]

            if self.varPolo1 != float('inf'):
                self.denominator = [1, -self.varPolo1]
            else:
                self.denominator = [1]

        else:
            if self.varCero1 != float('inf') and self.varCero2 != float('inf'):
                self.numerator = [1, -(self.varCero1 + self.varCero2), self.varCero1 * self.varCero2]
            elif self.varCero1 == float('inf') and self.varCero2 != float('inf'):
                self.numerator = [1, -self.varCero2]
            elif self.varCero1 != float('inf') and self.varCero2 == float('inf'):
                self.numerator = [1, -self.varCero1]
            else:
                self.numerator = [1]

            if self.varPolo1 != float('inf') and self.varPolo2 != float('inf'):
                self.denominator = [1, -(self.varPolo1 + self.varPolo2), self.varPolo1 * self.varPolo2]
            elif self.varPolo1 == float('inf') and self.varPolo2 != float('inf'):
                self.denominator = [1, -self.varPolo2]
            elif self.varPolo1 != float('inf') and self.varPolo2 == float('inf'):
                self.denominator = [1, -self.varPolo1]
            else:
                self.denominator = [1]

        if self.isGananciaMaxima == 0:
            self.H = ss.TransferFunction(np.dot(self.ganancia*self.normalizingFactor, self.numerator), self.denominator)
        else:
            self.H = ss.TransferFunction(self.numerator, self.denominator)
            self.bode = ss.bode(self.H, self.w)
            maxi = np.nanmax(self.bode[1])
            newFactor = np.power(10, -maxi/20)
            self.H = ss.TransferFunction(np.dot(newFactor*self.ganancia, self.numerator), self.denominator)

        if len(self.numerator) <= len(self.denominator):
            self.h = ss.impulse(self.H, T=self.t)
            self.sinRta = ss.lsim(self.H, U=self.varEntradaAmplitud * np.cos(
                self.varEntradaFrecuencia * self.t + self.varEntradaFase * 2 * np.pi / 360), T=self.t)
            self.stepRta = ss.lsim(self.H, U=self.varEntradaAmplitud * np.heaviside(self.t, 1), T=self.t)
            self.sqrRta = ss.lsim(self.H, U=self.varEntradaAmplitud * (
                        self.t / self.varEntradaPeriodo - np.floor(self.t / self.varEntradaPeriodo) > (
                            1 - self.varEntradaDutyCycle / 100)), T=self.t)
            self.renaming_filter()
        else:
            self.h = ss.impulse(self.NULL_H, T=self.t)
            self.sinRta = ss.lsim(self.NULL_H, U=self.varEntradaAmplitud * np.cos(
                self.varEntradaFrecuencia * self.t + self.varEntradaFase * 2 * np.pi / 360), T=self.t)
            self.stepRta = ss.lsim(self.NULL_H, U=self.varEntradaAmplitud * np.heaviside(self.t, 1), T=self.t)
            self.sqrRta = ss.lsim(self.NULL_H, U=self.varEntradaAmplitud * (
                        self.t / self.varEntradaPeriodo - np.floor(self.t / self.varEntradaPeriodo) > (
                            1 - self.varEntradaDutyCycle / 100)), T=self.t)
            self.labelTipoFiltro.setText(
                'ERROR!!! El sistema no es estable (H tiene numerador de mayor grado que su denominador')

        self.bode = ss.bode(self.H, self.w)
        if self.varEntrada == _ENTRADA_SENOIDE:
            self.rta = self.sinRta
        elif self.varEntrada == _ENTRADA_ESCALON:
            self.rta = self.stepRta
        else:
            self.rta = self.sqrRta

        self.update_pictures()

    def update_grado1_config_window(self):
        if self.varFiltro1er != _PRIMER_ORDEN_ARBRITRARIO:
            self.spinBoxPolo.setDisabled(1)
            self.spinBoxPoloIm.setDisabled(1)
            self.checkPolo_cero.setDisabled(1)
            self.checkPolo_infinito.setDisabled(1)

            self.spinBoxCero.setDisabled(1)
            self.spinBoxCeroIm.setDisabled(1)
            self.checkCero_cero.setDisabled(1)
            self.checkCero_infinito.setDisabled(1)
        else:
            self.spinBoxPolo.setDisabled(0)
            self.spinBoxPoloIm.setDisabled(0)
            self.checkPolo_cero.setDisabled(0)
            self.checkPolo_infinito.setDisabled(0)

            self.spinBoxCero.setDisabled(0)
            self.spinBoxCeroIm.setDisabled(0)
            self.checkCero_cero.setDisabled(0)
            self.checkCero_infinito.setDisabled(0)

    def update_grado2_config_window(self):
        if self.varFiltro2do != _SEGUNDO_ORDEN_ARBITRARIO:
            self.spinBoxPolo.setDisabled(1)
            self.spinBoxPoloIm.setDisabled(1)
            self.checkPolo_cero.setDisabled(1)
            self.checkPolo_infinito.setDisabled(1)
            self.spinBoxPolo_2.setDisabled(1)
            self.spinBoxPoloIm_2.setDisabled(1)
            self.checkPolo_cero_2.setDisabled(1)
            self.checkPolo_infinito_2.setDisabled(1)

            self.spinBoxCero.setDisabled(1)
            self.spinBoxCeroIm.setDisabled(1)
            self.checkCero_cero.setDisabled(1)
            self.checkCero_infinito.setDisabled(1)
            self.spinBoxCero_2.setDisabled(1)
            self.spinBoxCeroIm_2.setDisabled(1)
            self.checkCero_cero_2.setDisabled(1)
            self.checkCero_infinito_2.setDisabled(1)
        else:
            self.spinBoxPolo.setDisabled(0)
            self.spinBoxPoloIm.setDisabled(0)
            self.checkPolo_cero.setDisabled(0)
            self.checkPolo_infinito.setDisabled(0)
            self.spinBoxPolo_2.setDisabled(0)
            self.spinBoxPoloIm_2.setDisabled(0)
            self.checkPolo_cero_2.setDisabled(0)
            self.checkPolo_infinito_2.setDisabled(0)

            self.spinBoxCero.setDisabled(0)
            self.spinBoxCeroIm.setDisabled(0)
            self.checkCero_cero.setDisabled(0)
            self.checkCero_infinito.setDisabled(0)
            self.spinBoxCero_2.setDisabled(0)
            self.spinBoxCeroIm_2.setDisabled(0)
            self.checkCero_cero_2.setDisabled(0)
            self.checkCero_infinito_2.setDisabled(0)

        if self.varFiltro2do == _SEGUNDO_ORDEN_ARBITRARIO or self.varFiltro2do == _SEGUNDO_ORDEN_LOWPASS_NOTCH or self.varFiltro2do == _SEGUNDO_ORDEN_HIGHPASS_NOTCH:
            self.spinBoxFrecCorte_2.show()
            self.spinBoxAmortiguamiento_2.show()
        else:
            self.spinBoxFrecCorte_2.hide()
            self.spinBoxAmortiguamiento_2.hide()

    def update_grado_config_window(self):
        if self.varGrado == _PRIMER_ORDEN:
            self.spinBoxPolo_2.hide()
            self.spinBoxPoloIm_2.hide()
            self.checkPolo_cero_2.hide()
            self.checkPolo_infinito_2.hide()

            self.spinBoxCero_2.hide()
            self.spinBoxCeroIm_2.hide()
            self.checkCero_cero_2.hide()
            self.checkCero_infinito_2.hide()

            self.spinBoxFrecCorte_2.hide()
            self.labelAmortiguamiento.hide()
            self.spinBoxAmortiguamiento.hide()
            self.spinBoxAmortiguamiento_2.hide()

            self.combo1er.show()
            self.combo2do.hide()

            self.update_grado1_config_window()
        else:
            self.spinBoxPolo_2.show()
            self.spinBoxPoloIm_2.show()
            self.checkPolo_cero_2.show()
            self.checkPolo_infinito_2.show()

            self.spinBoxCero_2.show()
            self.spinBoxCeroIm_2.show()
            self.checkCero_cero_2.show()
            self.checkCero_infinito_2.show()

            self.spinBoxFrecCorte_2.show()
            self.labelAmortiguamiento.show()
            self.spinBoxAmortiguamiento.show()
            self.spinBoxAmortiguamiento_2.show()

            self.combo1er.hide()
            self.combo2do.show()

            self.update_grado2_config_window()

    def update_entrada_config_window(self):
        if self.varEntrada == _ENTRADA_SENOIDE:
            self.labelRtaFrecuencia.show()
            self.spinBoxRtaFrecuencia.show()
            self.labelRtaFase.show()
            self.spinBoxRtaFase.show()
            self.labelRtaPeriodo.hide()
            self.spinBoxRtaPeriodo.hide()
            self.labelRtaDuty.hide()
            self.spinBoxRtaDuty.hide()
        elif self.varEntrada == _ENTRADA_ESCALON:
            self.labelRtaFrecuencia.hide()
            self.spinBoxRtaFrecuencia.hide()
            self.labelRtaFase.hide()
            self.spinBoxRtaFase.hide()
            self.labelRtaPeriodo.hide()
            self.spinBoxRtaPeriodo.hide()
            self.labelRtaDuty.hide()
            self.spinBoxRtaDuty.hide()
        else:
            self.labelRtaFrecuencia.hide()
            self.spinBoxRtaFrecuencia.hide()
            self.labelRtaFase.hide()
            self.spinBoxRtaFase.hide()
            self.labelRtaPeriodo.show()
            self.spinBoxRtaPeriodo.show()
            self.labelRtaDuty.show()
            self.spinBoxRtaDuty.show()

    def update_pictures(self):
        self.axisBode1.clear()
        self.axisBode1.plot(self.bode[0], self.bode[1])
        self.axisBode1.grid()
        self.axisBode1.set_xscale('log')
        self.axisBode1.set_xlabel('Frecuencia')
        self.axisBode1.set_ylabel('Amplitud')
        self.figureBode1.suptitle('Diagrama de Bode: Amplitud')
        # self.axisBode1.legend(loc='lower left')
        self.canvasBode1.draw()

        # self.label.setText(str(np.nanmax(self.bode[1])))

        self.axisBode2.clear()
        self.axisBode2.plot(self.bode[0], self.bode[2])
        self.axisBode2.grid()
        self.axisBode2.set_xscale('log')
        self.axisBode2.set_xlabel('Frecuencia')
        self.axisBode2.set_ylabel('Fase')
        self.figureBode2.suptitle('Diagrama de Bode: Fase')
        self.canvasBode2.draw()

        self.axisPolosCeros.clear()
        self.axisPolosCeros.plot(0, 0, marker='.', color='k')
        if self.checkCero_infinito.isChecked() == 0:
            self.axisPolosCeros.plot(self.spinBoxCero.value(), self.spinBoxCeroIm.value(), marker='o', color='b')
        if self.checkPolo_infinito.isChecked() == 0:
            self.axisPolosCeros.plot(self.spinBoxPolo.value(), self.spinBoxPoloIm.value(), marker='X', color='r')
        if self.varGrado == _SEGUNDO_ORDEN:
            if self.checkCero_infinito_2.isChecked() == 0:
                self.axisPolosCeros.plot(self.spinBoxCero_2.value(), self.spinBoxCeroIm_2.value(), marker='o',
                                         color='b')
            if self.checkPolo_infinito_2.isChecked() == 0:
                self.axisPolosCeros.plot(self.spinBoxPolo_2.value(), self.spinBoxPoloIm_2.value(), marker='X',
                                         color='r')
        self.axisPolosCeros.grid()
        self.axisPolosCeros.set_xlabel('Eje real')
        self.axisPolosCeros.set_ylabel('Eje imaginario')
        self.figurePolosCeros.suptitle('Polos y ceros: plano s')
        self.canvasPolosCeros.draw()

        self.axisRespuesta.clear()
        self.axisRespuesta.plot(self.rta[0], self.rta[1])
        self.axisRespuesta.grid()
        self.axisRespuesta.set_xlabel('Tiempo')
        self.axisRespuesta.set_ylabel('Salida')
        self.figureRespuesta.suptitle('Respuesta en el tiempo')
        self.canvasRespuesta.draw()
