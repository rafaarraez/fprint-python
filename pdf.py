# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pdf.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QDialog
import pymongo
from arrow import utcnow, get
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

class Ui_pdf(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(320, 240)
        self.tipo = QtWidgets.QComboBox(Dialog)
        self.tipo.setGeometry(QtCore.QRect(30, 80, 261, 32))
        self.tipo.setObjectName("tipo")
        self.tipo.addItem("")
        self.tipo.addItem("")
        self.tipo.addItem("")
        self.tipo.addItem("")
        self.tipo.addItem("")
        self.pdf = QtWidgets.QPushButton(Dialog)
        self.pdf.setGeometry(QtCore.QRect(30, 140, 88, 34))
        self.pdf.setObjectName("pdf")
        self.cancelar = QtWidgets.QPushButton(Dialog)
        self.cancelar.setGeometry(QtCore.QRect(200, 140, 88, 34))
        self.cancelar.setObjectName("cancelar")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(80, 30, 171, 18))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.dialogo = Dialogo()


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.pdf.clicked.connect(self.crearPDF)
        self.cancelar.clicked.connect(self.cerrar)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Reportes"))
        self.tipo.setItemText(0, _translate("Dialog", "Seleccione un tipo usuario"))
        self.tipo.setItemText(1, _translate("Dialog", "Todos"))
        self.tipo.setItemText(2, _translate("Dialog", "Estudiantes"))
        self.tipo.setItemText(3, _translate("Dialog", "Profesores"))
        self.tipo.setItemText(4, _translate("Dialog", "Administrativo"))
        self.pdf.setText(_translate("Dialog", "Crear PDF"))
        self.cancelar.setText(_translate("Dialog", "Cancelar"))
        self.label.setText(_translate("Dialog", "Seleccione un usuario"))
    
    def crearPDF(self):

        valor = self.tipo.currentText()
        if valor == "Seleccione un tipo usuario":
            self.dialogo.etiqueta.setText("Seleccione un tipo de usuario primero")
            self.dialogo.exec_()
                 # ======================= CLASE reportePDF =========================

        class reportePDF(object):
            """Exportar una lista de diccionarios a una tabla en un
            archivo PDF."""
            
            def __init__(self, titulo, cabecera, datos, nombrePDF):
                super(reportePDF, self).__init__()

                self.titulo = titulo
                self.cabecera = cabecera
                self.datos = datos
                self.nombrePDF = nombrePDF

                self.estilos = getSampleStyleSheet()

            @staticmethod
            def _encabezadoPiePagina(canvas, archivoPDF):
                """Guarde el estado de nuestro lienzo para que podamos aprovecharlo"""
                
                canvas.saveState()
                estilos = getSampleStyleSheet()

                alineacion = ParagraphStyle(name="alineacion", alignment=TA_RIGHT,
                                            parent=estilos["Normal"])
        
                # Encabezado
                encabezadoNombre = Paragraph("UJAP", estilos["Normal"])
                anchura, altura = encabezadoNombre.wrap(archivoPDF.width, archivoPDF.topMargin)
                encabezadoNombre.drawOn(canvas, archivoPDF.leftMargin, 736)

                fecha = utcnow().to("local").format("dddd, DD - MMMM - YYYY", locale="es")
                fechaReporte = fecha.replace("-", "de")

                encabezadoFecha = Paragraph(fechaReporte, alineacion)
                anchura, altura = encabezadoFecha.wrap(archivoPDF.width, archivoPDF.topMargin)
                encabezadoFecha.drawOn(canvas, archivoPDF.leftMargin, 736)
        
                # Pie de página
                piePagina = Paragraph("Reporte generado para el control de asistencia UJAP.", estilos["Normal"])
                anchura, altura = piePagina.wrap(archivoPDF.width, archivoPDF.bottomMargin)
                piePagina.drawOn(canvas, archivoPDF.leftMargin, 15 * mm + (0.2 * inch))
        
                # Suelta el lienzo
                canvas.restoreState()

            def convertirDatos(self):
                """Convertir la lista de diccionarios a una lista de listas para crear
                la tabla PDF."""

                estiloEncabezado = ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,
                                                fontSize=10, textColor=white,
                                                fontName="Helvetica-Bold",
                                                parent=self.estilos["Normal"])

                estiloNormal = self.estilos["Normal"]
                estiloNormal.alignment = TA_LEFT

                claves, nombres = zip(*[[k, n] for k, n in self.cabecera])

                encabezado = [Paragraph(nombre, estiloEncabezado) for nombre in nombres]
                nuevosDatos = [tuple(encabezado)]

                for dato in self.datos:
                    nuevosDatos.append([Paragraph(str(dato[clave]), estiloNormal) for clave in claves])
                    
                return nuevosDatos
                
            def Exportar(self):
                """Exportar los datos a un archivo PDF."""

                alineacionTitulo = ParagraphStyle(name="centrar", alignment=TA_CENTER, fontSize=13,
                                                leading=10, textColor=purple,
                                                parent=self.estilos["Heading1"])
                
                self.ancho, self.alto = letter

                convertirDatos = self.convertirDatos()
            
                tabla = Table(convertirDatos, colWidths=(self.ancho-100)/len(self.cabecera), hAlign="CENTER")
                tabla.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0),(-1, 0), purple),
                    ("ALIGN", (0, 0),(0, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), # Texto centrado y alineado a la izquierda
                    ("INNERGRID", (0, 0), (-1, -1), 0.50, black), # Lineas internas
                    ("BOX", (0, 0), (-1, -1), 0.25, black), # Linea (Marco) externa
                    ]))

                historia = []
                historia.append(Paragraph(self.titulo, alineacionTitulo))
                historia.append(Spacer(1, 0.16 * inch))
                historia.append(tabla)

                archivoPDF = SimpleDocTemplate(self.nombrePDF, leftMargin=50, rightMargin=50, pagesize=letter,
                                            title="Reporte PDF", author="Rafael Arraez")
                
                try:
                    archivoPDF.build(historia, onFirstPage=self._encabezadoPiePagina,
                                    onLaterPages=self._encabezadoPiePagina,
                                    canvasmaker=numeracionPaginas)
                    
                # +------------------------------------+
                    return "Reporte generado con éxito."
                # +------------------------------------+
                except PermissionError:
                # +--------------------------------------------+  
                    return "Error inesperado: Permiso denegado."
                # +--------------------------------------------+


        # ================== CLASE numeracionPaginas =======================

        class numeracionPaginas(canvas.Canvas):
            def __init__(self, *args, **kwargs):
                canvas.Canvas.__init__(self, *args, **kwargs)
                self._saved_page_states = []

            def showPage(self):
                self._saved_page_states.append(dict(self.__dict__))
                self._startPage()

            def save(self):
                """Agregar información de la página a cada página (página x de y)"""
                numeroPaginas = len(self._saved_page_states)
                for state in self._saved_page_states:
                    self.__dict__.update(state)
                    self.draw_page_number(numeroPaginas)
                    canvas.Canvas.showPage(self)
                canvas.Canvas.save(self)
        
            def draw_page_number(self, conteoPaginas):
                self.drawRightString(204 * mm, 15 * mm + (0.2 * inch),
                                    "Página {} de {}".format(self._pageNumber, conteoPaginas))        

        # ===================== FUNCIÓN generarReporte =====================

        def generarReporte():
            """Ejecutar consulta a la base de datos (DB_USUARIOS) y llamar la función Exportar, la
            cuál esta en la clase reportePDF, a esta clase le pasamos el título de la tabla, la
            cabecera y los datos que llevará."""
            if valor == "Todos":
                myclient = pymongo.MongoClient("mongodb://localhost:27017/")
                mydb = myclient["ujap"]
                mycol = mydb["Marcaje"]

                datos = mycol.find()

                titulo = "Reporte de asistencia"

                cabecera = (
                    ("Nombre", "Nombre"),
                    ("Cedula", "Cedula"),
                    ("Username", "Username"),
                    ("Entrada", "Entrada"),
                    ("Salida", "Salida")
                    )
                
                fecha = utcnow().to("local").format("dddd, DD - MMMM - YYYY", locale="es")
                fechaArch = fecha.replace("-", "de")

                nombrePDF = "Reporte de asistencia " + fechaArch + ".pdf"

                reporte = reportePDF(titulo, cabecera, datos, nombrePDF).Exportar()
                print(reporte)
                self.dialogo.etiqueta.setText("Reporte general Guardado como PDF")
                self.dialogo.exec_()

            if valor == "Estudiantes":
                myclient = pymongo.MongoClient("mongodb://localhost:27017/")
                mydb = myclient["ujap"]
                mycol = mydb["Marcado_Estudiantes"]

                datos = mycol.find()

                titulo = "Reporte de asistencia de Estudiantes"

                cabecera = (
                    ("Nombre", "Nombre"),
                    ("Cedula", "Cedula"),
                    ("Username", "Username"),
                    ("Entrada", "Entrada"),
                    ("Salida", "Salida")
                    )
                
                fecha = utcnow().to("local").format("dddd, DD - MMMM - YYYY", locale="es")
                fechaArch = fecha.replace("-", "de")

                nombrePDF = "Reporte de asistencia de estudiantes " + fechaArch + ".pdf"

                reporte = reportePDF(titulo, cabecera, datos, nombrePDF).Exportar()
                print(reporte)
                self.dialogo.etiqueta.setText("Reporte de Estudiantes Guardado como PDF")
                self.dialogo.exec_()

            if valor == "Profesores":
                myclient = pymongo.MongoClient("mongodb://localhost:27017/")
                mydb = myclient["ujap"]
                mycol = mydb["Marcado_Profesores"]

                datos = mycol.find()

                titulo = "Reporte de asistencia de Profesores"

                cabecera = (
                    ("Nombre", "Nombre"),
                    ("Cedula", "Cedula"),
                    ("Username", "Username"),
                    ("Entrada", "Entrada"),
                    ("Salida", "Salida")
                    )
                
                fecha = utcnow().to("local").format("dddd, DD - MMMM - YYYY", locale="es")
                fechaArch = fecha.replace("-", "de")

                nombrePDF = "Reporte de asistencia de Profesores " + fechaArch + ".pdf"

                reporte = reportePDF(titulo, cabecera, datos, nombrePDF).Exportar()
                print(reporte)
                self.dialogo.etiqueta.setText("Reporte de Profesores Guardado como PDF")
                self.dialogo.exec_()

            if valor == "Administrativo":
                myclient = pymongo.MongoClient("mongodb://localhost:27017/")
                mydb = myclient["ujap"]
                mycol = mydb["Marcado_Administrativo"]

                datos = mycol.find()

                titulo = "Reporte de asistencia de Administrativo"

                cabecera = (
                    ("Nombre", "Nombre"),
                    ("Cedula", "Cedula"),
                    ("Username", "Username"),
                    ("Entrada", "Entrada"),
                    ("Salida", "Salida")
                    )
                
                fecha = utcnow().to("local").format("dddd, DD - MMMM - YYYY", locale="es")
                fechaArch = fecha.replace("-", "de")

                nombrePDF = "Reporte de asistencia de Administrativo " + fechaArch + ".pdf"

                reporte = reportePDF(titulo, cabecera, datos, nombrePDF).Exportar()
                print(reporte)
                self.dialogo.etiqueta.setText("Reporte de Administrativo Guardado como PDF")
                self.dialogo.exec_()


            # ======================== LLAMAR FUNCIÓN ==========================

        generarReporte()
    
    def cerrar(self):
        self.fileQuit()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_pdf()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())