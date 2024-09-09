import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from generatedApp import Ui_MainWindow

class MyApp(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("APLICACION")

        self.mainButton_visualizacion.clicked.connect(self.switch_pantallaVisualizacion)
        self.mainButton_DB.clicked.connect(self.switch_pantallaBaseDeDatos)
        self.mainButton_anadirArchivo.clicked.connect(self.switch_pantallaAnadirArchivo)

    def switch_pantallaVisualizacion(self): 
        self.stackedWidget.setCurrentIndex(0)
    
    def switch_pantallaBaseDeDatos(self): 
        self.stackedWidget.setCurrentIndex(1)

    def switch_pantallaAnadirArchivo(self): 
        self.stackedWidget.setCurrentIndex(2)

