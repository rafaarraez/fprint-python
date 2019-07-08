# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'admin.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(603, 555)
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(50, 19, 481, 521))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.agregar = QtWidgets.QPushButton(self.layoutWidget)
        self.agregar.setObjectName("agregar")
        self.verticalLayout.addWidget(self.agregar)
        self.eliminar = QtWidgets.QPushButton(self.layoutWidget)
        self.eliminar.setObjectName("eliminar")
        self.verticalLayout.addWidget(self.eliminar)
        self.actualizar = QtWidgets.QPushButton(self.layoutWidget)
        self.actualizar.setObjectName("actualizar")
        self.verticalLayout.addWidget(self.actualizar)
        self.huella = QtWidgets.QPushButton(self.layoutWidget)
        self.huella.setObjectName("huella")
        self.verticalLayout.addWidget(self.huella)
        self.basededatos = QtWidgets.QPushButton(self.layoutWidget)
        self.basededatos.setObjectName("basededatos")
        self.verticalLayout.addWidget(self.basededatos)
        self.pdf = QtWidgets.QPushButton(self.layoutWidget)
        self.pdf.setObjectName("pdf")
        self.verticalLayout.addWidget(self.pdf)
        self.graficos = QtWidgets.QPushButton(self.layoutWidget)
        self.graficos.setObjectName("graficos")
        self.verticalLayout.addWidget(self.graficos)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Administrador"))
        self.agregar.setText(_translate("Dialog", "Agregar usuario"))
        self.eliminar.setText(_translate("Dialog", "Eliminar Usuario"))
        self.actualizar.setText(_translate("Dialog", "Actualizar Datos"))
        self.huella.setText(_translate("Dialog", "Agregar Huella"))
        self.basededatos.setText(_translate("Dialog", "Cargar Base de datos"))
        self.pdf.setText(_translate("Dialog", "Generar Registros en formato PDF"))
        self.graficos.setText(_translate("Dialog", "Generar Grafica de Comportamiento"))

