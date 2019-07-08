# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'subir.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from os import getcwd, makedirs
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal, QFile
from PyQt5.QtWidgets import (QApplication, QDialog, QLabel, QPushButton, QFileDialog,
                             QLabel, QLineEdit, QMessageBox)
import os
import sys
import pandas as pd
import pymongo
import json

class Dialogo(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setFixedSize(300, 100)
        self.setWindowTitle("Mensaje")
        self.etiqueta = QLabel(self)

class Ui_db(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(320, 254)
        self.buscar = QtWidgets.QPushButton(Dialog)
        self.buscar.setGeometry(QtCore.QRect(60, 140, 101, 34))
        self.buscar.setObjectName("buscar")
        self.ruta = QtWidgets.QLineEdit(Dialog)
        self.ruta.setGeometry(QtCore.QRect(60, 80, 211, 32))
        self.ruta.setObjectName("ruta")
        self.subir = QtWidgets.QPushButton(Dialog)
        self.subir.setGeometry(QtCore.QRect(170, 140, 101, 34))
        self.subir.setObjectName("subir")
        self.dialogo = Dialogo()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.buscar.clicked.connect(self.upload_csv)
        self.subir.clicked.connect(self.import_content)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Seleccione un archivo"))
        self.buscar.setText(_translate("Dialog", "Buscar archivo"))
        self.subir.setText(_translate("Dialog", "Subir archivo"))

    def upload_csv(self):
        self.fname = QFileDialog.getOpenFileName(None, "Seleccionar un archivo .CSV", getcwd(),
                                                        "CSV data files (*.csv)",
                                                        options=QFileDialog.Options())
        print(self.fname)
        nombre = os.path.basename(str(self.fname))
        rut = os.path.dirname(str(self.fname))
        print("holaa",nombre)
        print("ruta",rut)
        aja = os.path.realpath(str(self.fname))
        print("AQUIIIIIIIIIIIIIII",aja)
        self.ruta.setText(str(self.fname))


    def import_content(self):
        mng_client = pymongo.MongoClient('localhost', 27017)
        mng_db = mng_client['ujap'] 
        collection_name = 'usuarios' 
        db_cm = mng_db[collection_name]
        filepath = self.ruta.text()
        cdir = os.path.dirname(__file__)
        file_res = os.path.join(cdir, filepath)
        data = pd.read_csv(file_res)
        data_json = json.loads(data.to_json(orient='records'))
        db_cm.remove()
        db_cm.insert(data_json)
        if data_json:
            self.dialogo.etiqueta.setText("Informacion cargada a la BD")
            self.dialogo.exec_()
        else:
            self.dialogo.etiqueta.setText("Hubo un error datos no cargados")
            self.dialogo.exec_() 

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_db()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
