# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'admin.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QDialog
from subir import Ui_db
from agregarHuella import Ui_Huella
import urllib
import numpy as np
import cv2
import pyzbar.pyzbar as pyzbar
import pyfprint
import requests
import base64
import pymongo
from arrow import utcnow, get
from pdf import Ui_pdf
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.colors import black, purple, white
from reportlab.pdfgen import canvas

class Dialogo(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.resize(300, 100)
        self.setWindowTitle("Mensaje")
        self.etiqueta = QLabel(self)

class Ui_admin(object):
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
        self.dialogo = Dialogo()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.basededatos.clicked.connect(self.cargar)
        self.agregar.clicked.connect(self.agregarUser)
        self.eliminar.clicked.connect(self.eliminarUser)
        self.huella.clicked.connect(self.agregarHuella)
        self.pdf.clicked.connect(self.menuPDF)
        self.graficos.clicked.connect(self.grafi)

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

    def cargar(self):
        self.cargarBD = QtWidgets.QMainWindow()
        self.ui = Ui_db()
        self.ui.setupUi(self.cargarBD)
        self.cargarBD.show()

    def agregarUser(self):
        # ip = input("Ingrese la ip de la camara: ")
        # url = 'http://'+ip+'/shot.jpg'  # Cambia esto por la ip de la camara
        url = 'http://10.113.222.163:8080/shot.jpg'  # Cambia esto por la ip de la camara
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["ujap"]
        mycol = mydb["usuarios"]


        def add_user():
            print("Se procedera a agregar un nuevo usuario al sistema. Por favor, siga las instrucciones\n")
            user = get_user_info()
            # user['huella'] = base64.encodebytes(get_finger()[0].data()[:]).decode('utf-8')
            x = mycol.insert_one(user)
            print("Se ha creado el usuario: ", user)

        def decode(frame):
            # Find barcodes and QR codes
            decoded_objects = pyzbar.decode(frame)

            if decoded_objects:
                obj_type = decoded_objects[0].type
                obj_data = None

                # Comprobar si es un QR
                if obj_type == 'QRCODE':
                    # Obtener informacion del QR
                    obj_data = decoded_objects[0].data

                return obj_data

            else:
                return None


        def get_user_info():
            user = None

            while not user:
                # Iniciar conexion a la Camara
                imgResp = urllib.request.urlopen(url)
                # imgResp = cv2.VideoCapture(0)
                imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
                frame = cv2.imdecode(imgNp, -1)

                bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Transformar imagen a Blanco y Negro
                qr_data = decode(bw)

                # Mostrar imagenes de la camara
                cv2.namedWindow('QR', cv2.WINDOW_NORMAL)
                cv2.resizeWindow('QR', 640, 420)
                cv2.imshow('QR', frame)

                if qr_data:
                    imgResp.close()
                    cv2.destroyAllWindows()
                    qr_data_decoded = qr_data.decode('utf-8')
                    lista = qr_data_decoded.split()
                    elements = len(lista)
                    user = {
                        "cedula": lista[2],
                        "nombre": " ".join(lista[3:elements-4]),
                        "correo": lista[elements-4],
                        "vencimiento": lista[elements-3],
                        "username": lista[elements-2],
                        "tipo": lista[elements-1]
                    }
                    myquery = user
                    if mycol.find_one(myquery):
                        print("Ya existe el usuario en la BD")
                        exit(0)

                # Leer keyboard input para cerrar la conexion
                if ord('q') == cv2.waitKey(10):
                    exit(0)
            return user

        # def get_finger():
        #     fp_reader = pyfprint.discover_devices()[0]
        #     fp_reader.open()
        #     print("Se procedera a escanear su dedo. Debera deslizar su dedo por el escaner hasta que se le indique")
        #     finger = fp_reader.enroll_finger()
        #     fp_reader.close()

        #     return finger


        add_user()

    def eliminarUser(self):
        # ip = input("Ingrese la ip de la camara: ")
        # url = 'http://'+ip+'/shot.jpg'  # Cambia esto por la ip de la camara
        url = 'http://10.113.222.163:8080/shot.jpg'  # Cambia esto por la ip de la camara
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["ujap"]
        mycol = mydb["usuarios"]


        def deleteUser():
            print("Se procedera a ELIMINAR un usuario al sistema. Por favor, siga las instrucciones\n")
            user = get_user_info()
            myquery = user
            aja = mycol.find_one(myquery)
            print(aja,"\n")
            if aja is None: 
                print("No existe el usuario")
            else:
                print("usuario = ",myquery)
                mycol.delete_one(myquery)
                print ("se elimino: ", user)

        def decode(frame):
            # Find barcodes and QR codes
            decoded_objects = pyzbar.decode(frame)

            if decoded_objects:
                obj_type = decoded_objects[0].type
                obj_data = None

                # Comprobar si es un QR
                if obj_type == 'QRCODE':
                    # Obtener informacion del QR
                    obj_data = decoded_objects[0].data

                return obj_data

            else:
                return None


        def get_user_info():
            user = None

            while not user:
                # Iniciar conexion a la Camara
                imgResp = urllib.request.urlopen(url)
                # imgResp = cv2.VideoCapture(0)
                imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
                frame = cv2.imdecode(imgNp, -1)

                bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Transformar imagen a Blanco y Negro
                qr_data = decode(bw)

                # Mostrar imagenes de la camara
                cv2.namedWindow('QR', cv2.WINDOW_NORMAL)
                cv2.resizeWindow('QR', 640, 420)
                cv2.imshow('QR', frame)

                if qr_data:
                    imgResp.close()
                    cv2.destroyAllWindows()
                    qr_data_decoded = qr_data.decode('utf-8')
                    lista = qr_data_decoded.split()
                    elements = len(lista)
                    user = {
                        "cedula": lista[2],
                        "nombre": " ".join(lista[3:elements-4]),
                        "correo": lista[elements-4],
                        "vencimiento": lista[elements-3],
                        "username": lista[elements-2],
                        "tipo": lista[elements-1]
                    }

                # Leer keyboard input para cerrar la conexion
                if ord('q') == cv2.waitKey(10):
                    exit(0)
            return user


        deleteUser()

    def agregarHuella(self):
        self.cargarBD = QtWidgets.QMainWindow()
        self.ui = Ui_Huella()
        self.ui.setupUi(self.cargarBD)
        self.cargarBD.show()        

    def menuPDF(self):
        self.cargarBD = QtWidgets.QMainWindow()
        self.ui = Ui_pdf()
        self.ui.setupUi(self.cargarBD)
        self.cargarBD.show()

    def grafi(self):
        print("Holas")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_admin()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())