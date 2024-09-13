from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QFileDialog,QApplication, QMainWindow, QTableWidget, QTableWidgetItem,QMessageBox
from generatedInterface import *  
from generatedDialog import *
import json
import sys

class MyApp(Ui_MainWindow):

    def __init__(self, window):
        self.setupUi(window)
        
        #Se encarga de setear los listener de los botones y los índices de los stackedWidgets
        self.setearInterfaz(window)

        #Se encarga de hacer la tabla de database bonita y dinámica
        self.database_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        #Importe de datos de prueba
        with open('pacientes.json', 'r', encoding='utf-8') as file:
            pacientes = json.load(file)

        self.loadData_database( pacientes)

        
    def setearInterfaz(self, window):
        # Seteo de los stackedWidgets al iniciar
        self.stackedWidget_submenuVisualizacion.setCurrentIndex(0)
        self.stackedWidgetPrincipal.setCurrentIndex(1)

        # Funciones anidadas para cambiar pantallas
        def switch_pantallaVisualizacion():
            self.stackedWidgetPrincipal.setCurrentIndex(0)

        def switch_pantallaBaseDeDatos():
            self.stackedWidgetPrincipal.setCurrentIndex(1)

        def switch_pantallaAnadirArchivo():
            self.stackedWidgetPrincipal.setCurrentIndex(2)

        def switch_subMenu_patient():
            self.stackedWidget_submenuVisualizacion.setCurrentIndex(0)

        def switch_subMenu_tools():
            self.stackedWidget_submenuVisualizacion.setCurrentIndex(1)

        # Setear Botones del menú principal
        self.mainButton_visualizacion.clicked.connect(switch_pantallaVisualizacion)
        self.mainButton_DB.clicked.connect(switch_pantallaBaseDeDatos)
        self.mainButton_anadirArchivo.clicked.connect(switch_pantallaAnadirArchivo)

        # Setear botones del submenu (Pantalla de visualización)
        self.subMenu_tools.clicked.connect(switch_subMenu_tools)
        self.subMenu_patient.clicked.connect(switch_subMenu_patient)

        # Setear botones de cargar de archivos (Pantalla de carga)
        self.archivoButton_carpeta.clicked.connect(self.cargar_dicom_carpeta)

    #Función encargada de cargar los pacientes en la tabla de base de datos
    def loadData_database(self, pacientes):
        self.database_table.setRowCount(len(pacientes))
        row = 0
        for paciente in pacientes:
            col = 0
            # Iterar sobre los valores del diccionario paciente
            for key, value in paciente.items():
                # Agregar cada valor a la columna correspondiente
                self.database_table.setItem(row, col, QtWidgets.QTableWidgetItem(str(value)))
                col += 1
            row += 1

    def cargar_dicom_carpeta(self):
        # Cuadro de diálogo para seleccionar una carpeta
        carpeta = QFileDialog.getExistingDirectory(None, 'Seleccionar carpeta con archivos DICOM')
        if carpeta:
            QMessageBox.information(None, 'Carpeta seleccionada', f'Has seleccionado la carpeta: {carpeta}')
            # Aquí puedes agregar la lógica para cargar todos los archivos DICOM de la carpeta



    def loadData_archivoDICOM(self, estudio):
        print("uwu")



#Inicialización de la aplicación y la ventana
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = MyApp(MainWindow)
MainWindow.show()
app.exec_()