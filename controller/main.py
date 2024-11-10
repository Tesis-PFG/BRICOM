from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QFileDialog,QApplication, QMainWindow, QTableWidget, QTableWidgetItem,QMessageBox
import view.generatedDialogCarga
from view.generatedInterface import *  
from view.generatedDialogTagsSubida import Ui_Dialog as Ui_DialogTagsSubida
from view.generatedDialogEscogerEstudio import Ui_Dialog as Ui_DialogEscogerEstudio
from view.generatedDialogCarga import Ui_Dialog as Ui_DialogCarga
from view.generatedDialogInicio import Ui_Dialog as Ui_DialogInicio
import ctypes
import shutil
import pydicom
import json
import sys, os, re
import model.config as config


class DicomProcessingThread(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, dicom_files, carpeta_origen, carpeta_modalidad, metadata_paciente, metadata_estudio, carpeta_paciente, modality):
        super().__init__()
        self.dicom_files = dicom_files
        self.carpeta_origen = carpeta_origen
        self.carpeta_modalidad = carpeta_modalidad
        self.metadata_paciente = metadata_paciente
        self.metadata_estudio = metadata_estudio
        self.carpeta_paciente = carpeta_paciente
        self.modality = modality
        
    def run(self):
        try:
            # Copiar y modificar todos los archivos DICOM
            for archivo in self.dicom_files:
                ruta_origen = os.path.join(self.carpeta_origen, archivo)
                ruta_destino = os.path.join(self.carpeta_modalidad, archivo)
                shutil.copy2(ruta_origen, ruta_destino)
                self.modificar_tags_dicom(ruta_destino, self.metadata_paciente, self.metadata_estudio)

            # Guardar metadata
            self.guardar_metadata(self.metadata_paciente, self.carpeta_paciente, "metadata_paciente.json")
            self.guardar_metadata(self.metadata_estudio, self.carpeta_paciente, f"metadata_{self.modality.upper()}.json")
            
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

    def modificar_tags_dicom(self, ruta_archivo, metadata_paciente, metadata_estudio):
        dicom_data = pydicom.dcmread(ruta_archivo)
        for tag, valor in {**metadata_paciente, **metadata_estudio}.items():
            if tag in dicom_data:
                dicom_data[tag].value = valor
        dicom_data.save_as(ruta_archivo)
    
    def guardar_metadata(self, metadata, ruta_carpeta, nombre_archivo):
        ruta_metadata = os.path.join(ruta_carpeta, nombre_archivo)
        with open(ruta_metadata, 'w') as f:
            json.dump(metadata, f, indent=4)

class MyApp(Ui_MainWindow):
    def __init__(self, window):

        # Guardar referencia a la ventana principal
        self.window = window
        
        # Hacer la ventana principal invisible y guardar su estado de ventana
        self.window_state = self.window.windowState()
        self.window.hide()
        
        # Guardar el tiempo de inicio
        self.start_time = QtCore.QTime.currentTime()
        
        # Crear y mostrar el diálogo de inicio
        self.dialogInicio = QtWidgets.QDialog(None)
        self.dialogInicio.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint | 
            QtCore.Qt.FramelessWindowHint
        )
        ui = Ui_DialogInicio()
        ui.setupUi(self.dialogInicio)
        self.dialogInicio.show()
        
        # Iniciar el proceso de carga
        QtCore.QTimer.singleShot(100, self.start_loading)

    def start_loading(self):
        # Configurar la interfaz principal manteniendo la ventana oculta
        self.setupUi(self.window)
        self.setearInterfaz(self.window)
        self.window.hide()
        
        # Iniciar la carga de datos
        QtCore.QTimer.singleShot(0, self.load_data)

    def load_data(self):
        # Cargar los datos
        self.loadData_database()
        
        # Calcular tiempo transcurrido
        elapsed = self.start_time.msecsTo(QtCore.QTime.currentTime())
        
        # Asegurar tiempo mínimo de 5 segundos
        remaining_time = max(5000 - elapsed, 0)
        QtCore.QTimer.singleShot(remaining_time, self.complete_loading)

    def complete_loading(self):
        # Cerrar el diálogo de inicio
        self.dialogInicio.close()
        
        # Restaurar el estado original de la ventana y mostrarla
        self.window.setWindowState(self.window_state)
        self.window.show()
        self.window.activateWindow()


    def setearInterfaz(self, window):
        current_dir = os.path.dirname(os.path.abspath(__file__))  # qt-int/controller/main

        # Definir la ruta del directorio raíz del proyecto
        project_dir = os.path.join(current_dir, '..')
        base_path = "model/local_database"
        path = os.path.join(project_dir, base_path)

        if not os.path.exists(path):
            os.makedirs(path)

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

        #Quita la posibilidad de editar las celdas
        self.patientInfo_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.studyInfo_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)




        # Setear Botones del menú principal
        self.mainButton_visualizacion.clicked.connect(switch_pantallaVisualizacion)
        self.mainButton_DB.clicked.connect(switch_pantallaBaseDeDatos)
        self.mainButton_anadirArchivo.clicked.connect(switch_pantallaAnadirArchivo)

        # Setear botones del submenu (Pantalla de visualización)
        self.subMenu_tools.clicked.connect(switch_subMenu_tools)
        self.subMenu_patient.clicked.connect(switch_subMenu_patient)

        # Setear botones de cargar de archivos (Pantalla de carga)
        self.archivoButton_carpeta.clicked.connect(self.procesar_dicom_carpeta)

        # Connect the cellClicked signal to open the patient selection dialog
        self.database_table.cellClicked.connect(self.open_patient_selection_dialog)
        
        # Ocultar botones de disposición por defecto
        disposition_buttons = [
            self.dispositionButton_1x2,
            self.dispositionButton_1x3,
            self.dispositionButton_2x1,
            self.dispositionButton_1u2d,
            self.dispositionButton_2x2,
            self.dispositionButton_1l2r,
            self.dispositionButton_3D
        ]
        for button in disposition_buttons:
            button.setVisible(False)


    #Función encargada de desplegar los pacientes en la tabla de base de datos
    def loadData_database(self):
        def leer_metadata_pacientes():
            current_dir = os.path.dirname(os.path.abspath(__file__))  # qt-int/controller/main        
            project_dir = os.path.join(current_dir, '..')  # Regresar dos niveles hacia el directorio raíz (qt-int)
            base_path = "model/local_database"
            path = os.path.join(project_dir, base_path)  # Combina el directorio del proyecto y la ruta relativa

            pacientes_metadata = {}

            # Recorrer las carpetas de pacientes
            for paciente_folder in os.listdir(path):  # Usa 'path' en lugar de 'base_path'
                paciente_path = os.path.join(path, paciente_folder)  # Usa 'path' en lugar de construir de nuevo

                # Asegurarse de que es un directorio
                if os.path.isdir(paciente_path):
                    metadata_paciente_file = os.path.join(paciente_path, "metadata_paciente.json")
                    
                    # Verificar si existe el archivo de metadata del paciente
                    if os.path.exists(metadata_paciente_file):
                        with open(metadata_paciente_file, 'r') as f:
                            metadata_paciente = json.load(f)
                        
                        # Añadir la metadata del paciente al diccionario de pacientes
                        pacientes_metadata[paciente_folder] = metadata_paciente
                    
                    # Recopilar información de las modalidades
                    modalidades = {}
                    for file in os.listdir(paciente_path):
                        if file.startswith("metadata_") and file.endswith(".json") and file != "metadata_paciente.json":
                            modalidad = file[9:-5]  # Extrae la modalidad del nombre del archivo
                            modalidad_file = os.path.join(paciente_path, file)
                            with open(modalidad_file, 'r') as f:
                                metadata_estudio = json.load(f)
                            modalidades[modalidad] = metadata_estudio
                    
                    # Añadir información de modalidades a la metadata del paciente
                    if paciente_folder in pacientes_metadata:
                        pacientes_metadata[paciente_folder]['modalidades'] = modalidades
                    else:
                        pacientes_metadata[paciente_folder] = {'modalidades': modalidades}

            print(pacientes_metadata)
            return pacientes_metadata
        
        def cargar_datos_en_tabla(pacientes):
            # Configurar el número de filas de la tabla de acuerdo a la cantidad de pacientes
            self.database_table.setRowCount(len(pacientes))

            # Ruta del ícono de la papelera
            icon_path_trash = "Assets/trash.png"
            icon = QtGui.QIcon(icon_path_trash)

            # Ajustar el tamaño predeterminado de las filas
            self.database_table.verticalHeader().setDefaultSectionSize(50)

            # Centramos todo el contenido de las celdas
            alignment = QtCore.Qt.AlignCenter

            row = 0
            for paciente_key, paciente_data in pacientes.items():
                # Extraer y formatear los valores específicos para cada columna
                nombre = paciente_data.get('PatientName', 'Desconocido').replace('^', ' ')
                id_paciente = paciente_data.get('PatientID', 'Desconocido')
                sexo = paciente_data.get('PatientSex', 'Desconocido')
                fecha_nacimiento = paciente_data.get('PatientBirthDate', 'Desconocido')
                if fecha_nacimiento != 'Desconocido':
                    fecha_nacimiento = f"{fecha_nacimiento[:4]}-{fecha_nacimiento[4:6]}-{fecha_nacimiento[6:]}"
                modalidades = ', '.join(paciente_data.get('modalidades', {}).keys())

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
                pb.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                pb.setIconSize(QtCore.QSize(48, 48))
                pb.setStyleSheet("""
                    QPushButton {
                        border: none;
                        background-color: transparent;
                    }
                """)
                pb.clicked.connect(lambda _, pid=id_paciente: delete_patient(pid))
                self.database_table.setCellWidget(row, 5, pb)  # Colocar el botón en la columna 5 (ícono de borrar)

                row += 1

            # Ajustar el tamaño de las filas para que se vea correctamente
            self.database_table.resizeRowsToContents()

        def filterData():
            filter_text = self.filterLiner_db.text().lower()
            
            filtered_pacientes = {}
            for paciente_key, paciente_data in config.all_patients.items():
                nombre = paciente_data.get('PatientName', '').replace('^', ' ').lower()
                id_paciente = paciente_data.get('PatientID', '').lower()
                
                if filter_text in nombre or filter_text in id_paciente:
                    filtered_pacientes[paciente_key] = paciente_data

            cargar_datos_en_tabla(filtered_pacientes)

        def delete_patient(patient_id):
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_dir = os.path.join(current_dir, '..')
            base_path = "model/local_database"
            path = os.path.join(project_dir, base_path)
            patient_folder = os.path.join(path, patient_id)
            reply = QMessageBox.question(None, 'Confirmar Eliminación',
                                        f'¿Está seguro que desea eliminar al paciente {patient_id}?\n'
                                        'Esta acción no se puede deshacer.',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                try:
                    shutil.rmtree(patient_folder)
                    if patient_id in config.all_patients:
                        del config.all_patients[patient_id]
                    self.loadData_database()
                    QMessageBox.information(None, 'Éxito', f'El paciente {patient_id} ha sido eliminado.')
                except Exception as e:
                    QMessageBox.critical(None, 'Error', f'No se pudo eliminar al paciente: {str(e)}')
            else:
                print("Eliminación cancelada.")
        
        # Cargar todos los pacientes
        config.all_patients = leer_metadata_pacientes()
        
        # Cargar datos iniciales en la tabla
        cargar_datos_en_tabla(config.all_patients)

        # Conectar el filterLiner_db con la función de filtrado
        self.filterLiner_db.textChanged.connect(filterData)

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


         # Obtener el directorio actual donde se encuentra este archivo
        current_dir = os.path.dirname(os.path.abspath(__file__))  # qt-int/controller/main
        
        # Definir la ruta del directorio raíz del proyecto
        project_dir = os.path.join(current_dir, '..')  # Regresar dos niveles hacia el directorio raíz (qt-int)

        # Crear la ruta a la carpeta model/local_database
        base_path = "model/local_database"
        carpeta_base = os.path.join(project_dir, base_path)  # Combina el directorio del proyecto y la ruta relativa

        # Variables de tags requeridos
        tags_requeridos_paciente = [
            "PatientName",
            "PatientID",
            "PatientBirthDate",
            "PatientSex",
            "PatientAge",
            "PatientWeight"
        ] 
        tags_requeridos_estudio = [
            "StudyID",
            "Modality",
            "StudyDate",
            "StudyTime",
            "InstitutionName",
            "StudyDescription"
        ]

        # Diálogo para búsqueda de archivo
        carpeta_origen = QFileDialog.getExistingDirectory(None, 'Seleccionar carpeta con archivos DICOM')

        # Validar selección de carpeta
        if not carpeta_origen:
            QtWidgets.QMessageBox.warning(None, 'Error', 'No se seleccionó ninguna carpeta.')
            return

        # Arreglo de archivos DICOM dentro de la carpeta escogida
        dicom_files = [f for f in os.listdir(carpeta_origen) if f.endswith('.dcm')]

        # Validar si se encontraron archivos DICOM
        if not dicom_files:
            QtWidgets.QMessageBox.warning(None, 'Error', 'No se encontraron archivos DICOM en la carpeta seleccionada.')
            return

        try:
            # Leer el primer archivo para obtener la información del paciente
            primer_archivo = os.path.join(carpeta_origen, dicom_files[0])
            dicom_data = pydicom.dcmread(primer_archivo)

            modality = str(dicom_data.Modality)

            # Extraer tags del primer archivo
            metadata_paciente = extraer_tags(dicom_data, tags_requeridos_paciente)
            metadata_estudio = extraer_tags(dicom_data, tags_requeridos_estudio)

            # Contar el número de imágenes DICOM
            num_imagenes = len(dicom_files)

            # Llamar a abrir_Pdialogo_tags con el número de imágenes
            metadata_paciente, metadata_estudio, dialogo_exitoso = self.abrir_Pdialogo_tags(metadata_paciente, metadata_estudio, num_imagenes)

            if dialogo_exitoso:
                    try:
                        # Abrir diálogo de carga
                        dialog, ui = self.abrir_dialogo_carga()
                        dialog.setModal(True)
                        dialog.setWindowFlags(QtCore.Qt.Window | 
                                            QtCore.Qt.WindowTitleHint | 
                                            QtCore.Qt.CustomizeWindowHint)
                        
                        dialog.show()
                        QtWidgets.QApplication.processEvents()

                        patient_id = metadata_paciente["PatientID"]
                        carpeta_paciente = crear_carpeta_paciente(carpeta_base, patient_id)
                        carpeta_modalidad = crear_carpeta_modalidad(carpeta_paciente, modality)

                        # Crear y configurar el hilo de procesamiento
                        self.processing_thread = DicomProcessingThread(
                            dicom_files,
                            carpeta_origen,
                            carpeta_modalidad,
                            metadata_paciente,
                            metadata_estudio,
                            carpeta_paciente,
                            modality
                        )
                        
                        # Conectar señales
                        self.processing_thread.finished.connect(
                            lambda: self.dicom_processing_finished(dialog, num_imagenes, carpeta_modalidad)
                        )
                        self.processing_thread.error.connect(
                            lambda error: self.dicom_processing_error(error, dialog)
                        )
                        
                        # Iniciar el procesamiento
                        self.processing_thread.start()

                    except Exception as e:
                        if dialog:
                            dialog.close()
                        QtWidgets.QMessageBox.critical(None, 'Error', f"Ocurrió un error al procesar los archivos: {str(e)}")

        except Exception as e:
            # Mostrar mensaje de error
            QtWidgets.QMessageBox.critical(None, 'Error', f"Ocurrió un error al procesar los archivos: {str(e)}")

        print("Procesamiento completado.")
        


    def dicom_processing_finished(self, dialog, num_imagenes, carpeta_modalidad):
        """Maneja la finalización exitosa del procesamiento"""
        dialog.close()
        QtWidgets.QMessageBox.information(None, 'Éxito', 
            f"Procesados {num_imagenes} archivos DICOM. Guardados en: {carpeta_modalidad}")
        print("Procesamiento completado.")

    def dicom_processing_error(self, error_message, dialog):
        """Maneja los errores durante el procesamiento"""
        dialog.close()
        QtWidgets.QMessageBox.critical(None, 'Error', 
            f"Ocurrió un error al procesar los archivos: {error_message}")


    def abrir_Pdialogo_tags(self, metadata_paciente, metadata_estudio, num_imagenes):

        def cargar_datos_en_tabla_tags(ui, metadata_paciente, metadata_estudio, tags_requeridos_paciente, tags_requeridos_estudio):
            # Configurar el número de filas de la tabla
            total_campos = len(tags_requeridos_paciente) + len(tags_requeridos_estudio)
            ui.uploadTags_table.setRowCount(total_campos)

            # Ruta del ícono de información
            icon_path_info = "Assets/trash.png"
            icon = QtGui.QIcon(icon_path_info)

            # Ajustar el tamaño predeterminado de las filas
            ui.uploadTags_table.verticalHeader().setDefaultSectionSize(40)

            # Ocultar los encabezados de las filas
            ui.uploadTags_table.verticalHeader().setVisible(False)

            # Crear una fuente Roboto
            font = QtGui.QFont("Roboto", 9)

            row = 0
            for metadata, tags_requeridos in [(metadata_paciente, tags_requeridos_paciente), (metadata_estudio, tags_requeridos_estudio)]:
                for campo in tags_requeridos:
                    valor = metadata.get(campo, "No encontrado")
                    
                    # Crear y alinear el item del campo
                    item_campo = QtWidgets.QTableWidgetItem(campo)
                    item_campo.setTextAlignment(QtCore.Qt.AlignCenter)
                    item_campo.setFont(font)
                    ui.uploadTags_table.setItem(row, 0, item_campo)

                    if campo == "Modality":
                        # Crear un QLabel para el valor no editable de Modality
                        label = QtWidgets.QLabel(str(valor))
                        label.setAlignment(QtCore.Qt.AlignCenter)
                        label.setFont(font)
                        label.setStyleSheet("""
                            QLabel {
                                border: 1px solid #A0A0A0;
                                border-radius: 5px;
                                padding: 2px;
                                background-color: #F0F0F0;
                            }
                        """)
                        ui.uploadTags_table.setCellWidget(row, 1, label)
                    else:
                        # Crear un QLineEdit para el valor editable
                        line_edit = QtWidgets.QLineEdit(str(valor))
                        line_edit.setAlignment(QtCore.Qt.AlignCenter)
                        line_edit.setFont(font)
                        line_edit.setStyleSheet("""
                            QLineEdit {
                                border: 1px solid #A0A0A0;
                                border-radius: 5px;
                                padding: 2px;
                                background-color: white;
                            }
                        """)
                        ui.uploadTags_table.setCellWidget(row, 1, line_edit)

                    # Insertar el botón con ícono de información
                    pb = QtWidgets.QPushButton()
                    pb.setIcon(icon)
                    pb.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                    pb.setIconSize(QtCore.QSize(24, 24))
                    pb.setStyleSheet("""
                        QPushButton {
                            border: none;
                            background-color: transparent;
                        }
                    """)
                    ui.uploadTags_table.setCellWidget(row, 2, pb)

                    row += 1

            # Ajustar el tamaño de las columnas
            ui.uploadTags_table.setColumnWidth(0, 200)  # Ancho fijo para la columna "Campo"
            ui.uploadTags_table.setColumnWidth(1, 300)  # Ancho fijo para la columna "Valor"
            ui.uploadTags_table.setColumnWidth(2, 40)   # Ancho fijo para la columna del ícono

            # Ajustar el tamaño de las columnas
            ui.uploadTags_table.setColumnWidth(0, 200)  # Ancho fijo para la columna "Campo"
            ui.uploadTags_table.setColumnWidth(1, 300)  # Ancho fijo para la columna "Valor"
            ui.uploadTags_table.setColumnWidth(2, 40)   # Ancho fijo para la columna del ícono

        dialog = QtWidgets.QDialog()
        dialog.setWindowFlags(dialog.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        ui = Ui_DialogTagsSubida()
        ui.setupUi(dialog)

        # Actualizar el label con el número de imágenes
        ui.numImagenes.setText(f"Imágenes cargadas: {num_imagenes}")

        tags_requeridos_paciente = ["PatientName", "PatientID", "PatientBirthDate", "PatientSex", "PatientAge", "PatientWeight"]
        tags_requeridos_estudio = ["StudyID", "Modality", "StudyDate", "StudyTime", "InstitutionName", "StudyDescription"]

        ui.uploadTags_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        cargar_datos_en_tabla_tags(ui, metadata_paciente, metadata_estudio, tags_requeridos_paciente, tags_requeridos_estudio)

        # Conectar los botones a las funciones correspondientes
        ui.acceptButton_uploadTags.clicked.connect(dialog.accept)
        ui.cancelButton_uploadTags.clicked.connect(dialog.reject)

        result = dialog.exec_()

        if result == QtWidgets.QDialog.Accepted:
            # Si se presionó el botón de aceptar, actualizar los metadatos
            updated_metadata_paciente = {}
            updated_metadata_estudio = {}
            
            for row in range(ui.uploadTags_table.rowCount()):
                campo = ui.uploadTags_table.item(row, 0).text()
                valor = ui.uploadTags_table.cellWidget(row, 1).text()
                
                if campo in tags_requeridos_paciente:
                    updated_metadata_paciente[campo] = valor
                elif campo in tags_requeridos_estudio:
                    updated_metadata_estudio[campo] = valor

            return updated_metadata_paciente, updated_metadata_estudio, True
        else:
            # Si se presionó el botón de cancelar o se cerró el diálogo
            return {}, {}, False
    

    def open_patient_selection_dialog(self, row, column):
        dialog = QtWidgets.QDialog()
        dialog.setWindowFlags(dialog.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        ui =  Ui_DialogEscogerEstudio()
        ui.setupUi(dialog)

        def update_study_buttons(patient_id):
            # Obtener rutas
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_dir = os.path.join(current_dir, '..')
            base_path = "model/local_database"
            path = os.path.join(project_dir, base_path)
            patient_folder = os.path.join(path, patient_id)
            
            # Verificar existencia de estudios
            has_ct = os.path.exists(os.path.join(patient_folder, "metadata_CT.json"))
            has_mr = os.path.exists(os.path.join(patient_folder, "metadata_MR.json"))
            
            # Mostrar/ocultar botones según disponibilidad de estudios
            ui.CTButton_paciente.setVisible(has_ct)
            ui.MRButton_paciente.setVisible(has_mr)
            ui.ImagenConjuntaButton_paciente.setVisible(has_ct and has_mr)

        def update_info_tables(patient_id, study_type=None):
            # Load patient data
            current_dir = os.path.dirname(os.path.abspath(__file__))  # qt-int/controller/main

            # Definir la ruta del directorio raíz del proyecto
            project_dir = os.path.join(current_dir, '..')
            base_path = "model/local_database"
            path = os.path.join(project_dir, base_path)
            
            patient_folder = os.path.join(path, patient_id)
            patient_metadata_file = os.path.join(patient_folder, "metadata_paciente.json")


            if os.path.exists(patient_metadata_file):
                with open(patient_metadata_file, 'r') as f:
                    patient_data = json.load(f)
                
                # Update patientInfo_table
                self.patientInfo_table.setRowCount(len(patient_data))
                for row, (key, value) in enumerate(patient_data.items()):
                    self.patientInfo_table.setItem(row, 0, QTableWidgetItem(key))
                    self.patientInfo_table.setItem(row, 1, QTableWidgetItem(str(value)))
            
            # Load study data if a study type is selected
            if study_type:
                study_metadata_file = os.path.join(patient_folder, f"metadata_{study_type.upper()}.json")
                if os.path.exists(study_metadata_file):
                    with open(study_metadata_file, 'r') as f:
                        study_data = json.load(f)
                    
                    # Update studyInfo_table
                    self.studyInfo_table.setRowCount(len(study_data))
                    for row, (key, value) in enumerate(study_data.items()):
                        self.studyInfo_table.setItem(row, 0, QTableWidgetItem(key))
                        self.studyInfo_table.setItem(row, 1, QTableWidgetItem(str(value)))
                else:
                    # Clear study table if no study data is found
                    self.studyInfo_table.setRowCount(0)
            else:
                # Clear study table if no study type is selected
                self.studyInfo_table.setRowCount(0)

        def set_current_study(study_type, patien_id):

            # Set the current patient and study
            config.current_study = study_type
            config.current_patient = patient_id
            print(f"Current patient: {config.current_patient}, Current study: {config.current_study}")

            update_info_tables(config.current_patient, study_type)
            dialog.accept()  # Close the dialog after selection
            self.set_enabled_views(True)
            self.set_enabled_tools(False)
            #self.hide_studies()
            #self.clear_layout()            

            # Lista de botones de disposición
            disposition_buttons = [
                self.dispositionButton_1x2,
                self.dispositionButton_1x3,
                self.dispositionButton_2x1,
                self.dispositionButton_1u2d,
                self.dispositionButton_2x2,
                self.dispositionButton_1l2r,
                self.dispositionButton_3D
            ]

            # Controlar la visibilidad de los botones de disposición
            for button in disposition_buttons:
                if study_type.lower() == "imagenconjunta":
                    button.setVisible(True)
                    #Esconde la información del estudio
                    self.frame_19.setVisible(False)
                else:
                    button.setVisible(False)
                    #Muestra la información del estudio
                    self.frame_19.setVisible(True)

            # Se resetea la vista de los estudios
            self.uncheck_tools()
            self.clear_tools()
            self.uncheck_views()
            self.clear_layout()

            #Cambio de pantalla a visualización
            self.stackedWidgetPrincipal.setCurrentIndex(0)
            self.stackedWidget_submenuVisualizacion.setCurrentIndex(0)
            self.mainButton_visualizacion.setChecked(True)
            self.subMenu_patient.setChecked(True)
            
            
            

        def navigate_patient(direction):
            new_row = row + direction
            if 0 <= new_row < self.database_table.rowCount():
                dialog.accept()  # Close the current dialog
                self.database_table.selectRow(new_row)
                self.open_patient_selection_dialog(new_row, 0)
            else:
                QMessageBox.information(dialog, "Navegación", "No hay más pacientes en esta dirección.")

    
        # Get patient data from the selected row
        patient_name = self.database_table.item(row, 0).text()
        patient_id = self.database_table.item(row, 1).text()
        patient_sex = self.database_table.item(row, 2).text()
        patient_birth_date = self.database_table.item(row, 3).text()

        # Set patient information in the dialog
        ui.nombre_label.setText(f"Nombre: {patient_name}")
        ui.idPaciente_label.setText(f"ID: {patient_id}")
        ui.sexo_label.setText(f"Sexo: {patient_sex}")
        ui.fechaNacimiento_label.setText(f"Fecha de Nacimiento: {patient_birth_date}")

        update_study_buttons(patient_id)

        # Connect buttons to their respective functions
        ui.MRButton_paciente.clicked.connect(lambda: set_current_study("MR", patient_id))
        ui.CTButton_paciente.clicked.connect(lambda: set_current_study("CT", patient_id))
        ui.ImagenConjuntaButton_paciente.clicked.connect(lambda: set_current_study("ImagenConjunta", patient_id))
        
        ui.anteriorButton_paciente.clicked.connect(lambda: navigate_patient(-1))
        ui.siguienteButton_paciente.clicked.connect(lambda: navigate_patient(1))

        dialog.exec_()
    
    def abrir_dialogo_carga(self):
        dialog = QtWidgets.QDialog()
        dialog.setWindowFlags(Qt.FramelessWindowHint)
        ui = Ui_DialogCarga()
        ui.setupUi(dialog)
        
        # Obtener el directorio actual donde se encuentra este archivo
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Construir la ruta al GIF está una carpeta arriba y luego en 'assets'
        gif_path = os.path.join(current_dir, "..", "assets", "carga_gif.gif")
        
        # Verificar si el archivo existe
        if os.path.exists(gif_path):
            # Crear y configurar el QMovie
            movie = QtGui.QMovie(gif_path)
            
            # Opcional: ajustar el tamaño del GIF
            movie.setScaledSize(QtCore.QSize(100, 100))  # Ajusta estos números según necesites
            
            # Asignar el QMovie al QLabel
            ui.label_3.setMovie(movie)

            # Opcional: centrar el GIF en el label
            ui.label_3.setAlignment(QtCore.Qt.AlignCenter)
            
            # Iniciar la animación
            movie.start()
        else:
            print(f"No se encontró el archivo GIF en: {gif_path}")
        
        dialog.setModal(True)
        dialog.setWindowFlags(QtCore.Qt.Window | 
                            QtCore.Qt.WindowTitleHint | 
                            QtCore.Qt.CustomizeWindowHint)
        
        return dialog, ui
    

#Inicialización de la aplicación y la ventana
# Configurar el ID de la aplicación en Windows
if sys.platform == 'win32':
    myappid = u'javeriana.bricom.v1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

app = QtWidgets.QApplication(sys.argv)
app.setApplicationName('BRICOM')
app.setWindowIcon(QIcon(".\\Assets/BRICOM_logo.ico"))

MainWindow = QtWidgets.QMainWindow()
MainWindow.setWindowTitle("BRICOM")  
MainWindow.setWindowIcon(QIcon(".\\Assets/BRICOM_logo.ico"))  

ui = MyApp(MainWindow)
app.exec_()