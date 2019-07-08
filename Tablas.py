import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pandas import DataFrame

class Window(QMainWindow):

    def __init__(self, parent = None):
        super(Window,self).__init__(parent)
        self.Table_of_widgets()

    def Table_of_widgets(self):

        rowCount = 20
        columnCount = 4

        self.table = QTableWidget()
        self.table.setColumnCount(columnCount)
        self.table.setRowCount(rowCount)
        self.table.setHorizontalHeaderLabels(['Nombre', 'User', 'Entrada', 'Salida'])
        self.table.verticalHeader().hide()

        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)


        self.table.showMaximized()

      

##    def onCurrentTextChanged(self, text):
##        self.comboB.clear()
##        elements = fin1
##        if isinstance(elements, list):
##            self.comboB.addItems(elements)
##        else:
##            self.comboB.addItem(elements)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setApplicationName('MyWindow')
    main = Window()
    sys.exit(app.exec_())