from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QFileDialog,QApplication, QMainWindow, QTableWidget, QTableWidgetItem,QMessageBox
from generatedInterface import *  
from generatedDialog import *
import shutil
import pydicom
import json
import sys, os, re


class MyApp(Ui_MainWindow):

    def __init__(self, window):
        self.setupUi(window)
        
        #Se encarga de setear los listener de los botones y los índices de los stackedWidgets
        self.setearInterfaz(window)
        self.loadData_database()


    #Función encargarda de inicializar la interfaz, los botones y las pantallas
    def setearInterfaz(self, window):
        # Funciones anidadas para cambiar pantallas
        def switch_pantallaVisualizacion():
            self.stackedWidgetPrincipal.setCurrentIndex(0)

        def switch_pantallaBaseDeDatos():
            self.loadData_database()
            self.stackedWidgetPrincipal.setCurrentIndex(1)

        def switch_pantallaAnadirArchivo():
            self.stackedWidgetPrincipal.setCurrentIndex(2)

        def switch_subMenu_patient():
            self.stackedWidget_submenuVisualizacion.setCurrentIndex(0)

        def switch_subMenu_tools():
            self.stackedWidget_submenuVisualizacion.setCurrentIndex(1)

        # Seteo de los stackedWidgets al iniciar
        self.stackedWidget_submenuVisualizacion.setCurrentIndex(0)
        self.stackedWidgetPrincipal.setCurrentIndex(1)

        #Se encarga de hacer la tabla de database bonita y dinámica
        self.database_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Setear Botones del menú principal
        self.mainButton_visualizacion.clicked.connect(switch_pantallaVisualizacion)
        self.mainButton_DB.clicked.connect(switch_pantallaBaseDeDatos)
        self.mainButton_anadirArchivo.clicked.connect(switch_pantallaAnadirArchivo)

        # Setear botones del submenu (Pantalla de visualización)
        self.subMenu_tools.clicked.connect(switch_subMenu_tools)
        self.subMenu_patient.clicked.connect(switch_subMenu_patient)

        # Setear botones de cargar de archivos (Pantalla de carga)
        self.archivoButton_carpeta.clicked.connect(self.procesar_dicom_carpeta)

    #Función encargada de desplegar los pacientes en la tabla de base de datos
    def loadData_database(self):

        def leer_metadata_pacientes():
            base_path = "local_database"
            pacientes_metadata = {}

            # Recorrer las carpetas de pacientes
            for paciente_folder in os.listdir(base_path):
                paciente_path = os.path.join(base_path, paciente_folder)
                
                # Asegurarse de que es un directorio
                if os.path.isdir(paciente_path):
                    metadata_file = os.path.join(paciente_path, "metadata.json")
                    
                    # Verificar si existe el archivo de metadata
                    if os.path.exists(metadata_file):
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                        
                        # Añadir la metadata al diccionario de pacientes
                        pacientes_metadata[paciente_folder] = metadata
                    
                    # Recopilar información de las modalidades
                    modalidades = {}
                    for modalidad_folder in os.listdir(paciente_path):
                        modalidad_path = os.path.join(paciente_path, modalidad_folder)
                        if os.path.isdir(modalidad_path):
                            # Contar los archivos DICOM en la carpeta de modalidad
                            dicom_files = [f for f in os.listdir(modalidad_path) if f.endswith('.dcm')]
                            modalidades[modalidad_folder] = len(dicom_files)
                    
                    # Añadir información de modalidades a la metadata del paciente
                    if paciente_folder in pacientes_metadata:
                        pacientes_metadata[paciente_folder]['modalidades'] = modalidades
                    else:
                        pacientes_metadata[paciente_folder] = {'modalidades': modalidades}

            print(pacientes_metadata)
            return pacientes_metadata
        
        def cargar_datos_en_tabla( pacientes):
                # Configurar el número de filas de la tabla de acuerdo a la cantidad de pacientes
                self.database_table.setRowCount(len(pacientes))

                # Ruta del ícono de la papelera
                icon_path_trash = "Assets/trash.png"
                icon = QtGui.QIcon(icon_path_trash)

                # Ajustar el tamaño predeterminado de las filas
                self.database_table.verticalHeader().setDefaultSectionSize(50)  # Cambia este valor para hacer las filas más grandes

                # Centramos todo el contenido de las celdas
                alignment = QtCore.Qt.AlignCenter

                row = 0
                for paciente_key, paciente_data in pacientes.items():
                    # Extraer y formatear los valores específicos para cada columna
                    nombre = paciente_data['PatientName'].replace('^', ' ')  
                    id_paciente = paciente_data['PatientID']
                    sexo = paciente_data['PatientSex']
                    fecha_nacimiento = f"{paciente_data['PatientBirthDate'][:4]}-{paciente_data['PatientBirthDate'][4:6]}-{paciente_data['PatientBirthDate'][6:]}"  # Formato YYYY-MM-DD
                    modalidades = ', '.join(paciente_data['modalidades'].keys())

                    # Crear y centrar cada valor en su respectiva columna
                    item_nombre = QtWidgets.QTableWidgetItem(nombre)
                    item_nombre.setTextAlignment(alignment)
                    self.database_table.setItem(row, 0, item_nombre)  # Columna "Nombre"

                    item_id_paciente = QtWidgets.QTableWidgetItem(id_paciente)
                    item_id_paciente.setTextAlignment(alignment)
                    self.database_table.setItem(row, 1, item_id_paciente)  # Columna "ID_Paciente"

                    item_sexo = QtWidgets.QTableWidgetItem(sexo)
                    item_sexo.setTextAlignment(alignment)
                    self.database_table.setItem(row, 2, item_sexo)  # Columna "Sexo"

                    item_fecha_nacimiento = QtWidgets.QTableWidgetItem(fecha_nacimiento)
                    item_fecha_nacimiento.setTextAlignment(alignment)
                    self.database_table.setItem(row, 3, item_fecha_nacimiento)  # Columna "Fecha_nacimiento"

                    item_modalidades = QtWidgets.QTableWidgetItem(modalidades)
                    item_modalidades.setTextAlignment(alignment)
                    self.database_table.setItem(row, 4, item_modalidades)  # Columna "Modalidades"

                    # Insertar el botón con ícono de borrar
                    pb = QtWidgets.QPushButton()
                    pb.setIcon(icon)
                    pb.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))  # Cambiar el cursor a "hand pointing"
                    pb.setIconSize(QtCore.QSize(48, 48))  # Ajusta el tamaño del ícono

                    # Estilo para eliminar el fondo y el borde del botón
                    pb.setStyleSheet("""
                        QPushButton {
                            border: none;
                            background-color: transparent;
                        }
                    """)
                    self.database_table.setCellWidget(row, 5, pb)  # Colocar el botón en la columna 5 (ícono de borrar)

                    row += 1

                # Ajustar el tamaño de las filas para que se vea correctamente
                self.database_table.resizeRowsToContents()
        
        pacientes_db = leer_metadata_pacientes()
        cargar_datos_en_tabla(pacientes_db)

    #Función encargada de cargar los archivos a la base de datos local
    def procesar_dicom_carpeta(self, tags_requeridos):
        def extraer_tags(dicom_data, tags_requeridos):
            """Extrae los tags especificados del archivo DICOM basado en sus nombres."""
            metadata = {}
            
            for tag_dicom in tags_requeridos:
                if tag_dicom in dicom_data:
                    metadata[tag_dicom] = str(dicom_data.data_element(tag_dicom).value)
                else:
                    metadata[tag_dicom] = "No encontrado"
            
            return metadata

        def limpiar_nombre(nombre):
            # Eliminar caracteres no alfanuméricos excepto espacios
            nombre_limpio = re.sub(r'[^a-zA-Z0-9\s]', '', nombre)
            # Reemplazar espacios múltiples por un solo espacio
            nombre_limpio = re.sub(r'\s+', ' ', nombre_limpio)
            # Limitar la longitud y eliminar espacios al inicio y final
            return nombre_limpio[:50].strip()

        def crear_carpeta_paciente(carpeta_base, patient_id):
            
            id_limpio = re.sub(r'[^a-zA-Z0-9]', '', patient_id)
            folder_name = f"{id_limpio}"
            carpeta_paciente = os.path.join(carpeta_base, folder_name)
            if not os.path.exists(carpeta_paciente):
                os.makedirs(carpeta_paciente)
            return carpeta_paciente

        def crear_carpeta_modalidad(carpeta_paciente, modality):
            modality_limpia = limpiar_nombre(modality)
            carpeta_modalidad = os.path.join(carpeta_paciente, modality_limpia)
            if not os.path.exists(carpeta_modalidad):
                os.makedirs(carpeta_modalidad)
            return carpeta_modalidad

        def copiar_archivos_dicom(rutas_origen, carpeta_destino):
            for ruta in rutas_origen:
                shutil.copy2(ruta, carpeta_destino)

        def guardar_metadata(metadata, ruta_carpeta):
            ruta_metadata = os.path.join(ruta_carpeta, "metadata.json")
            with open(ruta_metadata, 'w') as f:
                json.dump(metadata, f, indent=4)

        #Variables Iniciales
        carpeta_base = "local_database"
        tags_requeridos_paciente = ["PatientName", "PatientID", "PatientBirthDate", "PatientSex", "PatientAge"] 
        tags_requeridos_estudio=["StudyID", "Modality", "StudyDate", "StudyTime", "InstitutionName"]

        #Dialogo para búsqueda de archivo
        carpeta_origen = QFileDialog.getExistingDirectory(None, 'Seleccionar carpeta con archivos DICOM')
        
        #El usuario no escogió ninguna carpeta
        if not carpeta_origen:
            QtWidgets.QMessageBox.warning(None, 'Error', 'No se seleccionó ninguna carpeta.')
            return

        #Crear la carpeta de local_database en caso de que no exista
        if not os.path.exists(carpeta_base):
            os.makedirs(carpeta_base)

        #Arreglo de archivos DICOM dentro de la carpeta escogida
        dicom_files = [f for f in os.listdir(carpeta_origen) if f.endswith('.dcm')]

        #El arreglo de archivos DICOM está vacío, ya que la carpeta no tenía nada
        if not dicom_files:
            QtWidgets.QMessageBox.warning(None, 'Error', 'No se encontraron archivos DICOM en la carpeta seleccionada.')
            return

        try:
            # Leer el primer archivo para obtener la información del paciente
            primer_archivo = os.path.join(carpeta_origen, dicom_files[0])
            dicom_data = pydicom.dcmread(primer_archivo)

            patient_name = str(dicom_data.PatientName)
            patient_id = str(dicom_data.PatientID)
            modality = str(dicom_data.Modality)

            carpeta_paciente = crear_carpeta_paciente(carpeta_base, patient_id)
            carpeta_modalidad = crear_carpeta_modalidad(carpeta_paciente, modality)

            # Copiar todos los archivos DICOM
            rutas_origen = [os.path.join(carpeta_origen, f) for f in dicom_files]
            copiar_archivos_dicom(rutas_origen, carpeta_modalidad)

            # Extraer tags del primer archivo
            metadata_paciente = extraer_tags(dicom_data, tags_requeridos_paciente)
            metadata_estudio = extraer_tags(dicom_data, tags_requeridos_estudio)

            print(metadata_estudio)
            print(metadata_paciente)
            # Guardar metadata
            guardar_metadata(metadata_paciente, carpeta_paciente)
            guardar_metadata(metadata_estudio, carpeta_modalidad)

            # Mostrar mensaje de éxito
            QtWidgets.QMessageBox.information(None, 'Éxito', f"Procesados {len(dicom_files)} archivos DICOM. Guardados en: {carpeta_modalidad}")
        except Exception as e:
            # Mostrar mensaje de error
            QtWidgets.QMessageBox.critical(None, 'Error', f"Ocurrió un error al procesar los archivos: {str(e)}")

        print("Procesamiento completado.")

#Inicialización de la aplicación y la ventana
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = MyApp(MainWindow)
MainWindow.show()
app.exec_()