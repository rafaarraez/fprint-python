# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'usuario.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import time
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QDialog
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal

import urllib
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import requests
import pyfprint
import base64
import pymongo

from admin import Ui_admin

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

class Ui_User(object):
    def setupUi(self, Dialog):
        object.__init__(self)
        Dialog.setObjectName("Dialog")
        self.foto = QtWidgets.QLabel(Dialog)
        self.foto.setGeometry(QtCore.QRect(30, 20, 161, 161))
        Dialog.setFixedSize(527,384)
        self.foto.setFrameShape(QtWidgets.QFrame.Box)
        self.foto.setText("")
        self.foto.setObjectName("foto")
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(240, 60, 251, 131))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.nombre = QtWidgets.QLineEdit(self.layoutWidget)
        self.nombre.setEnabled(False)
        self.nombre.setObjectName("nombre")
        self.verticalLayout.addWidget(self.nombre)
        self.cedula = QtWidgets.QLineEdit(self.layoutWidget)
        self.cedula.setEnabled(False)
        self.cedula.setObjectName("cedula")
        self.verticalLayout.addWidget(self.cedula)
        self.username = QtWidgets.QLineEdit(self.layoutWidget)
        self.username.setEnabled(False)
        self.username.setObjectName("username")
        self.verticalLayout.addWidget(self.username)
        self.layoutWidget1 = QtWidgets.QWidget(Dialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(40, 210, 451, 151))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btn_entrada = QtWidgets.QPushButton(self.layoutWidget1)
        self.btn_entrada.setObjectName("btn_entrada")
        self.verticalLayout_2.addWidget(self.btn_entrada)
        self.btn_salida = QtWidgets.QPushButton(self.layoutWidget1)
        self.btn_salida.setObjectName("btn_salida")
        self.verticalLayout_2.addWidget(self.btn_salida)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 2, 1)
        self.entrada = QtWidgets.QLineEdit(self.layoutWidget1)
        self.entrada.setEnabled(False)
        self.entrada.setObjectName("entrada")
        self.gridLayout.addWidget(self.entrada, 0, 1, 1, 1)
        self.salida = QtWidgets.QLineEdit(self.layoutWidget1)
        self.salida.setEnabled(False)
        self.salida.setObjectName("salida")
        self.gridLayout.addWidget(self.salida, 1, 1, 1, 1)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(240, 10, 251, 36))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_mrc = QtWidgets.QPushButton(self.widget)
        self.btn_mrc.setObjectName("btn_mrc")
        self.horizontalLayout.addWidget(self.btn_mrc)
        self.btn_admin = QtWidgets.QPushButton(self.widget)
        self.btn_admin.setObjectName("btn_admin")
        self.horizontalLayout.addWidget(self.btn_admin)
        self.dialogo = Dialogo()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.btn_mrc.clicked.connect(self.btn)
        self.btn_entrada.clicked.connect(self.Marcar_entrada)
        self.btn_salida.clicked.connect(self.Marcar_salida)
        self.btn_admin.clicked.connect(self.admin)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Bienvenido"))
        self.btn_entrada.setText(_translate("Dialog", "Entrada"))
        self.btn_salida.setText(_translate("Dialog", "Salida"))
        self.btn_mrc.setText(_translate("Dialog", "Marcar Asistenccia"))
        self.btn_admin.setText(_translate("Dialog", "Area Admin"))

    def btn(self):
        def add_user():
            user = get_user_info()
            self.entrada.setText("")
            self.salida.setText("")
            # user['huella'] = base64.encodebytes(get_finger()[0].data()[:]).decode('utf-8')
            myquery = user
            if mycol.find_one(myquery):
                self.dialogo.etiqueta.setText("Deslice su huella")
                self.dialogo.exec_()
                print("Ya existe el usuario en la BD")
                self.nombre.setText(user['nombre'])
                self.cedula.setText(user['cedula'])
                self.username.setText(user['username'])
                self.tipo = user['tipo']
                self.name = user['nombre']
                nombre = user['nombre']
                if nombre == 'RAFAEL EDUARDO ARRAEZ GUEVARA':
                    label = self.foto
                    pixi = QtGui.QPixmap('fotos/rafa.jpg').scaled(160, 160, QtCore.Qt.KeepAspectRatio)
                    label.setPixmap(pixi)
                else:
                    if nombre == 'IVAN FERNANDO DE MENEZES HURTADO':
                        label = self.foto
                        pixi = QtGui.QPixmap('fotos/ivan.jpg').scaled(160, 160, QtCore.Qt.KeepAspectRatio)
                        label.setPixmap(pixi)
                    else:
                        if nombre == 'JEAN PIER MOBAYED KOUNBOZ':
                            label = self.foto
                            pixi = QtGui.QPixmap('fotos/jean.jpg').scaled(160, 160, QtCore.Qt.KeepAspectRatio)
                            label.setPixmap(pixi)
                        else:
                            label = self.foto
                            pixi = QtGui.QPixmap('fotos/paez.jpg').scaled(160, 160, QtCore.Qt.KeepAspectRatio)
                            label.setPixmap(pixi)
                
                self.dialogo.etiqueta.setText("sesion iniciada")
                self.dialogo.exec_()
            else:
                self.dialogo.etiqueta.setText("Informacion no encontrada en la BD")
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

    def aja(self):

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


        def scan_qr():
            cedula = None

            while not cedula:
                # Iniciar conexion a la Camara
                imgResp = urllib.request.urlopen(url)
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
                    cedula = qr_data_decoded.split(' ')[2]

                # Leer keyboard input para cerrar la conexion
                if ord('q') == cv2.waitKey(10):
                    exit(0)
            return cedula


        def get_huella(cedula):
            myquery = { "cedula": cedula }
            myquery = mycol.find(myquery)
            for x in mydoc:
                nombre = x['nombre']
                if nombre == 'RAFAEL EDUARDO ARRAEZ GUEVARA':
                    label = self.foto
                    pixi = QtGui.QPixmap('rafa.jpg').scaled(160, 160, QtCore.Qt.KeepAspectRatio)
                    label.setPixmap(pixi)
                if nombre == 'IVAN FERNANDO DE MENEZES HURTADO':
                    label = self.foto
                    pixi = QtGui.QPixmap('ivan.jpg').scaled(160, 160, QtCore.Qt.KeepAspectRatio)
                    label.setPixmap(pixi)
                if nombre == 'JEAN PIER MOBAYED KOUNBOZ':
                    label = self.foto
                    pixi = QtGui.QPixmap('jean.jpg').scaled(160, 160, QtCore.Qt.KeepAspectRatio)
                    label.setPixmap(pixi)
                print(x['nombre'])
                huella_decoded = x['huella']
                        # print("HUELLA: \n", huella_decoded)
                huella_b64 = huella_decoded.encode('utf-8')
                return base64.decodebytes(huella_b64)
            else:
                return None   


        def verify_identity(huella):
            print(mydoc['correo'])
            pyfprint.init()
            fp_reader = pyfprint.discover_devices()[0]
            finger = pyfprint.Fprint(huella)
            print('Deslice su dedo por el lector para verificar su identidad')
            self.dialogo.etiqueta.setText("Deslice el dedo sobre el lector")
            self.dialogo.exec_()
            fp_reader.open()
            is_verified = fp_reader.verify_finger(finger)[0]
            fp_reader.close()
            pyfprint.exit()
            return is_verified

        cedula = scan_qr()
        huella = get_huella(cedula)
        if huella:
            if verify_identity(huella):
                print('Sesion iniciada')
            else:
                print('Su huella no es la almacenada en la BD')
                self.dialogo.etiqueta.setText("No encuentra su huella en la BD")
                self.dialogo.exec_()
        else:
            print('Su informacion no coincide con ninguno de los usuarios en la BD')
            self.dialogo.etiqueta.setText("Informacion no encontrada en la BD")
            self.dialogo.exec_()

    def Marcar_entrada(self):
        mycol = mydb['Marcaje']
        nombr = self.nombre.text()
        cedul = self.cedula.text()
        user = self.username.text()
        myquery = { "Nombre": nombr }
        mydoc = mycol.find(myquery)
        
        for x in mycol.find():
            print(x)
        
        myquery = { "Nombre": nombr,
                    "Salida": "" }

        mydoc = mycol.find(myquery)
        salidaa = 0
        for x in mydoc:
            salidaa = x['Salida']
            print(x)


        ahora = time.strftime("%c")
        if nombr == "":
            self.dialogo.etiqueta.setText("Inicie sesion primero")
            self.dialogo.exec_()
        else:
            if salidaa == "":
                self.dialogo.etiqueta.setText("Marque salida")
                self.dialogo.exec_() 
            else:    
                if self.entrada.text() == "" and salidaa == 0:
                    if self.entrada.text() == "":
                        self.entrada.setText(ahora)

                        marcado_entrada = {
                            "Nombre": nombr,
                            "Cedula": cedul,
                            "Username": user,
                            "Entrada": ahora,
                            "Salida": ""
                        }
                        mycol.insert_one(marcado_entrada)
                        if self.tipo == "ESTUDIANTE":
                            mycol = mydb['Marcado_Estudiantes']
                            mycol.insert_one(marcado_entrada)
                        if self.tipo == "PROFESORES":
                            mycol = mydb['Marcado_Profesores']
                            mycol.insert_one(marcado_entrada)
                        if self.tipo == "ADMINISTRATIVO":
                            mycol = mydb['Marcado_Administrativo']
                            mycol.insert_one(marcado_entrada)
                    else:
                        if aja == "":
                            self.dialogo.etiqueta.setText("Debe marcar su salida primero antes.")
                            self.dialogo.exec_()
                else:
                    self.dialogo.etiqueta.setText("Ya realizo el marcado")
                    self.dialogo.exec_()
        
    def Marcar_salida(self):
        mycol = mydb['Marcaje']
        nombr = self.nombre.text()
        cedul = self.cedula.text()
        user = self.username.text()

        myquery = { "Nombre": nombr,
                    "Salida": "" }

        mydoc = mycol.find(myquery)
        entradaa = 0
        for x in mydoc:
            entradaa = x['Entrada']
            print(x)

        ahora = time.strftime("%c")

        if nombr == "":
            self.dialogo.etiqueta.setText("Inicie sesion primero")
            self.dialogo.exec_()

        else:
            if entradaa == 0:
                self.dialogo.etiqueta.setText("Marque Entrada primero")
                self.dialogo.exec_() 
            else:
                if self.salida.text() == "":
                    self.salida.setText(ahora)
                    marcado_Salida = {"$set" : {"Salida": ahora} }

                    mycol.update_one(myquery, marcado_Salida)

                    if self.tipo == "ESTUDIANTE":
                        mycol = mydb['Marcado_Estudiantes']
                        mycol.update_one(myquery, marcado_Salida)

                    if self.tipo == "PROFESORES":
                        mycol = mydb['Marcado_Profesores']
                        mycol.update_one(myquery, marcado_Salida)

                    if self.tipo == "ADMINISTRATIVO":
                        mycol = mydb['Marcado_Administrativo']
                        mycol.update_one(myquery, marcado_Salida)

                else:
                    self.dialogo.etiqueta.setText("Ya realizo el marcado")
                    self.dialogo.exec_()
        
    def admin(self):
        nombre = self.nombre.text()
        if nombre == "":
            self.dialogo.etiqueta.setText("Inicie sesion primero")
            self.dialogo.exec_()
        else:
            name_user = self.name
            if name_user != 'RAFAEL EDUARDO ARRAEZ GUEVARA':
                self.dialogo.etiqueta.setText("no es admin")
                self.dialogo.exec_()
            else:
                self.actualizarVtn = QtWidgets.QMainWindow()
                self.ui = Ui_admin()
                self.ui.setupUi(self.actualizarVtn)
                self.actualizarVtn.show() 

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_User()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
