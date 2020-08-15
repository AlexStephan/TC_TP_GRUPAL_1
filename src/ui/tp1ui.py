# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tp1ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(998, 644)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.habilitarSegundoGrafico_CheckBox = QtWidgets.QCheckBox(Form)
        self.habilitarSegundoGrafico_CheckBox.setObjectName("habilitarSegundoGrafico_CheckBox")
        self.verticalLayout.addWidget(self.habilitarSegundoGrafico_CheckBox)
        self.selectorGraficoEntrada_ComboBox = QtWidgets.QComboBox(Form)
        self.selectorGraficoEntrada_ComboBox.setObjectName("selectorGraficoEntrada_ComboBox")
        self.selectorGraficoEntrada_ComboBox.addItem("")
        self.selectorGraficoEntrada_ComboBox.addItem("")
        self.selectorGraficoEntrada_ComboBox.addItem("")
        self.verticalLayout.addWidget(self.selectorGraficoEntrada_ComboBox)
        self.funcionTransferencia_PushButton = QtWidgets.QPushButton(Form)
        self.funcionTransferencia_PushButton.setObjectName("funcionTransferencia_PushButton")
        self.verticalLayout.addWidget(self.funcionTransferencia_PushButton)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.Numerador_LineEdit = QtWidgets.QLineEdit(Form)
        self.Numerador_LineEdit.setObjectName("Numerador_LineEdit")
        self.verticalLayout_3.addWidget(self.Numerador_LineEdit)
        self.Denominador_LineEdit = QtWidgets.QLineEdit(Form)
        self.Denominador_LineEdit.setObjectName("Denominador_LineEdit")
        self.verticalLayout_3.addWidget(self.Denominador_LineEdit)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_desde = QtWidgets.QLabel(Form)
        self.label_desde.setObjectName("label_desde")
        self.verticalLayout_5.addWidget(self.label_desde)
        self.spinBox_desde = QtWidgets.QDoubleSpinBox(Form)
        self.spinBox_desde.setMinimum(-100.0)
        self.spinBox_desde.setMaximum(100.0)
        self.spinBox_desde.setObjectName("spinBox_desde")
        self.verticalLayout_5.addWidget(self.spinBox_desde)
        self.horizontalLayout_6.addLayout(self.verticalLayout_5)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_hasta = QtWidgets.QLabel(Form)
        self.label_hasta.setObjectName("label_hasta")
        self.verticalLayout_6.addWidget(self.label_hasta)
        self.spinBox_hasta = QtWidgets.QDoubleSpinBox(Form)
        self.spinBox_hasta.setMinimum(-100.0)
        self.spinBox_hasta.setMaximum(100.0)
        self.spinBox_hasta.setObjectName("spinBox_hasta")
        self.verticalLayout_6.addWidget(self.spinBox_hasta)
        self.horizontalLayout_6.addLayout(self.verticalLayout_6)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_pasos = QtWidgets.QLabel(Form)
        self.label_pasos.setObjectName("label_pasos")
        self.verticalLayout_7.addWidget(self.label_pasos)
        self.spinBox_pasos = QtWidgets.QSpinBox(Form)
        self.spinBox_pasos.setMinimum(1)
        self.spinBox_pasos.setMaximum(1000000000)
        self.spinBox_pasos.setObjectName("spinBox_pasos")
        self.verticalLayout_7.addWidget(self.spinBox_pasos)
        self.horizontalLayout_6.addLayout(self.verticalLayout_7)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.OK_Hs_PushButton = QtWidgets.QPushButton(Form)
        self.OK_Hs_PushButton.setMaximumSize(QtCore.QSize(40, 16777215))
        self.OK_Hs_PushButton.setObjectName("OK_Hs_PushButton")
        self.horizontalLayout_5.addWidget(self.OK_Hs_PushButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_3.addWidget(self.line_2)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.spice_PushButton = QtWidgets.QPushButton(Form)
        self.spice_PushButton.setObjectName("spice_PushButton")
        self.verticalLayout.addWidget(self.spice_PushButton)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.spice_List = QtWidgets.QListWidget(Form)
        self.spice_List.setMinimumSize(QtCore.QSize(479, 306))
        self.spice_List.setObjectName("spice_List")
        self.verticalLayout_4.addWidget(self.spice_List)
        self.verticalLayout.addLayout(self.verticalLayout_4)
        self.medicion_PushButton = QtWidgets.QPushButton(Form)
        self.medicion_PushButton.setObjectName("medicion_PushButton")
        self.verticalLayout.addWidget(self.medicion_PushButton)
        self.borrarGraficos_PushButton = QtWidgets.QPushButton(Form)
        self.borrarGraficos_PushButton.setObjectName("borrarGraficos_PushButton")
        self.verticalLayout.addWidget(self.borrarGraficos_PushButton)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.graficoSuperior_StackedWidget = QtWidgets.QStackedWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graficoSuperior_StackedWidget.sizePolicy().hasHeightForWidth())
        self.graficoSuperior_StackedWidget.setSizePolicy(sizePolicy)
        self.graficoSuperior_StackedWidget.setObjectName("graficoSuperior_StackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.graficoSuperior_StackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.graficoSuperior_StackedWidget.addWidget(self.page_2)
        self.verticalLayout_2.addWidget(self.graficoSuperior_StackedWidget)
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setMinimumSize(QtCore.QSize(0, 60))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.navigation1 = QtWidgets.QHBoxLayout()
        self.navigation1.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.navigation1.setObjectName("navigation1")
        self.horizontalLayout_2.addLayout(self.navigation1)
        self.verticalLayout_2.addWidget(self.frame)
        self.graficoInferior_StackedWidget = QtWidgets.QStackedWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graficoInferior_StackedWidget.sizePolicy().hasHeightForWidth())
        self.graficoInferior_StackedWidget.setSizePolicy(sizePolicy)
        self.graficoInferior_StackedWidget.setObjectName("graficoInferior_StackedWidget")
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.graficoInferior_StackedWidget.addWidget(self.page_3)
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.graficoInferior_StackedWidget.addWidget(self.page_4)
        self.verticalLayout_2.addWidget(self.graficoInferior_StackedWidget)
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 60))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.navigation2 = QtWidgets.QHBoxLayout()
        self.navigation2.setObjectName("navigation2")
        self.horizontalLayout_3.addLayout(self.navigation2)
        self.verticalLayout_2.addWidget(self.frame_2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.habilitarSegundoGrafico_CheckBox.setText(_translate("Form", "Segundo gráfico"))
        self.selectorGraficoEntrada_ComboBox.setItemText(0, _translate("Form", "Entrada de gráfico superior"))
        self.selectorGraficoEntrada_ComboBox.setItemText(1, _translate("Form", "Entrada de gráfico inferior"))
        self.selectorGraficoEntrada_ComboBox.setItemText(2, _translate("Form", "Entrada de Bodes"))
        self.funcionTransferencia_PushButton.setText(_translate("Form", "H(s)"))
        self.Numerador_LineEdit.setPlaceholderText(_translate("Form", "Numerador"))
        self.Denominador_LineEdit.setPlaceholderText(_translate("Form", "Denominador"))
        self.label_desde.setText(_translate("Form", "Desde"))
        self.label_hasta.setText(_translate("Form", "Hasta"))
        self.label_pasos.setText(_translate("Form", "Pasos"))
        self.OK_Hs_PushButton.setText(_translate("Form", "OK"))
        self.spice_PushButton.setText(_translate("Form", "SPICE"))
        self.medicion_PushButton.setText(_translate("Form", "Medición (csv)"))
        self.borrarGraficos_PushButton.setText(_translate("Form", "BORRAR GRÁFICOS"))
        self.label.setText(_translate("Form", "Plot Tool Grupo 2"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
