# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'agregarHuella.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QDialog
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
import urllib
import numpy as np
import cv2
import pyzbar.pyzbar as pyzbar
import pyfprint
import requests
import base64
import pymongo

url = 'http://10.172.49.153:8080/shot.jpg'  # Cambia esto por la ip de la camara
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["ujap"]
mycol = mydb["usuarios"]

class Dialogo(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.resize(300, 100)
        self.setWindowTitle("Mensaje")
        self.etiqueta = QLabel(self)

class Ui_Huella(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(320, 240)
        self.btn_huella = QtWidgets.QPushButton(Dialog)
        self.btn_huella.setGeometry(QtCore.QRect(80, 140, 171, 34))
        self.btn_huella.setObjectName("btn_huella")
        self.mensaje = QtWidgets.QLabel(Dialog)
        self.mensaje.setGeometry(QtCore.QRect(110, 100, 111, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.mensaje.setFont(font)
        self.mensaje.setText("")
        self.mensaje.setObjectName("mensaje")
        self.dialogo = Dialogo()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.btn_huella.clicked.connect(self.addHuella)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate

        self.btn_huella.setText(_translate("Dialog", "Agregar Huella"))

    def addHuella(self):
        def add_user():
            user = get_user_info()
            # user['huella'] = base64.encodebytes(get_finger()[0].data()[:]).decode('utf-8')
            myquery = user
            if mycol.find_one(myquery):
                self.dialogo.etiqueta.setText("Deslice su huella")
                self.dialogo.exec_()
                print("Ya existe el usuario en la BD")
                self.dialogo.etiqueta.setText("Huella Agregada")
                self.dialogo.exec_()
                
                
            
            

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

        # def get_finger():
        #     fp_reader = pyfprint.discover_devices()[0]
        #     fp_reader.open()
        #     print("Se procedera a escanear su dedo. Debera deslizar su dedo por el escaner hasta que se le indique")
        #     finger = fp_reader.enroll_finger()
        #     fp_reader.close()
        #     self.mensaje.setText("Deslice su dedo sobre el lector")
        #     return finger



        add_user()