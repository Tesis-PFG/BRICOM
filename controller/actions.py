from PyQt5 import QtWidgets, QtCore
from app.interface.QtOrthoViewer import *
from app.interface.QtSegmentationViewer import *
from app.interface.VtkBase import *
from app.interface.ViewersConnection import *
from app.interface.mat_3d import registro
from model.Dicom_vis.DicomViewer import *
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QPoint
import model.config as config
from view.Render3DMHD import *
from PyQt5.QtCore import QThread, pyqtSignal
import os

from view.generatedDialogCarga import Ui_Dialog as Ui_DialogCarga
from PyQt5 import QtGui


class ImageProcessingThread(QThread):
    finished = pyqtSignal(str)  # Emite el path del archivo procesado
    error = pyqtSignal(str)
    
    def __init__(self, file_paths, file_paths_2):
        super().__init__()
        self.file_paths = file_paths
        self.file_paths_2 = file_paths_2
        
    def run(self):
        try:
            # Ejecutar el registro (asumiendo que es una función importada)
            registro(self.file_paths, self.file_paths_2)
            # Emitir la señal con el path del archivo resultante
            self.finished.emit('./Data/raw/patient.mhd')
        except Exception as e:
            self.error.emit(str(e))


class ViewerActions:
    def __init__(self, frame_3, dcm_viewer, viewers, ViewersConnection, vtkBaseClass):
        self.frame_3 = frame_3
        self.dcm_viewer = dcm_viewer
        self.QtSagittalOrthoViewer, self.QtAxialOrthoViewer, self.QtCoronalOrthoViewer, self.QtSegmentationViewer = viewers
        self.ViewersConnection = ViewersConnection
        self.vtkBaseClass = vtkBaseClass
        self.structure = 0
        self.views = [self.QtSagittalOrthoViewer, self.QtAxialOrthoViewer, self.QtCoronalOrthoViewer]
        self.frames = {}  # Diccionario para almacenar frames de cada visualizador
        self.create_frames()

        # Verifica si frame_3 ya tiene un layout; si no, crea uno nuevo.
        if not self.frame_3.layout():
            layout = QtWidgets.QHBoxLayout(self.frame_3)  # Usa un QHBoxLayout para alinear a la izquierda
            layout.setAlignment(Qt.AlignLeft)  # Alineación a la izquierda
            self.frame_3.setLayout(layout)

    def create_frames(self):
        visualizadores = [self.dcm_viewer, self.QtSagittalOrthoViewer, self.QtAxialOrthoViewer,
                          self.QtCoronalOrthoViewer, self.QtSegmentationViewer]
        nombres = ["dcm_viewer", "QtSagittalOrthoViewer", "QtAxialOrthoViewer",
                   "QtCoronalOrthoViewer", "QtSegmentationViewer"]

        # Crear un QFrame para cada visualizador y ocultarlo por defecto
        for visualizador, nombre in zip(visualizadores, nombres):
            frame = QtWidgets.QFrame(self.frame_3)
            layout = QtWidgets.QVBoxLayout(frame)
            layout.addWidget(visualizador)
            frame.setVisible(False)
            self.frames[nombre] = frame

    def clear_layout(self):
        if self.frame_3.layout() is not None:
            while self.frame_3.layout().count():
                child = self.frame_3.layout().takeAt(0)
                if child.widget() and type(child.widget()) == 'QSplitter':
                    self.frame_3.layout().removeWidget(child.widget())
        for frame in self.frames.values():
            frame.setVisible(False)

    def display_one_image(self):
        self.clear_layout()
        if config.current_study in ['CT', 'MR']:
            self.frames["dcm_viewer"].setVisible(True)
            self.frame_3.layout().addWidget(self.frames["dcm_viewer"])
        elif config.current_study == 'ImagenConjunta':
            self.frames["QtSagittalOrthoViewer"].setVisible(True)
            self.frame_3.layout().addWidget(self.frames["QtSagittalOrthoViewer"])

        self.frame_3.layout().update()
        self.frame_3.update()
        self.open_data()

    def display_two_images_vertical(self):
        self.clear_layout()
        vertical_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        
        self.frames["QtSagittalOrthoViewer"].setVisible(True)
        self.frames["QtAxialOrthoViewer"].setVisible(True)
        
        vertical_splitter.addWidget(self.frames["QtSagittalOrthoViewer"])
        vertical_splitter.addWidget(self.frames["QtAxialOrthoViewer"])
        self.frame_3.layout().addWidget(vertical_splitter)

        self.frame_3.layout().update()
        self.open_data()

    def display_two_images_horizontal(self):
        self.clear_layout()
        horizontal_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        self.frames["QtSagittalOrthoViewer"].setVisible(True)
        self.frames["QtAxialOrthoViewer"].setVisible(True)
        
        horizontal_splitter.addWidget(self.frames["QtSagittalOrthoViewer"])
        horizontal_splitter.addWidget(self.frames["QtAxialOrthoViewer"])
        self.frame_3.layout().addWidget(horizontal_splitter)

        self.frame_3.layout().update()
        self.open_data()

    def display_three_images_horizontal(self):
        self.clear_layout()
        horizontal_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        self.frames["QtSagittalOrthoViewer"].setVisible(True)
        self.frames["QtAxialOrthoViewer"].setVisible(True)
        self.frames["QtCoronalOrthoViewer"].setVisible(True)

        horizontal_splitter.addWidget(self.frames["QtSagittalOrthoViewer"])
        horizontal_splitter.addWidget(self.frames["QtAxialOrthoViewer"])
        horizontal_splitter.addWidget(self.frames["QtCoronalOrthoViewer"])
        self.frame_3.layout().addWidget(horizontal_splitter)

        self.frame_3.layout().update()
        self.open_data()

    def display_three_images_t(self):
        self.clear_layout()
        vertical_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        horizontal_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        self.frames["QtSagittalOrthoViewer"].setVisible(True)
        self.frames["QtAxialOrthoViewer"].setVisible(True)
        self.frames["QtCoronalOrthoViewer"].setVisible(True)

        vertical_splitter.addWidget(self.frames["QtSagittalOrthoViewer"])
        vertical_splitter.addWidget(self.frames["QtCoronalOrthoViewer"])
        horizontal_splitter.addWidget(vertical_splitter)
        horizontal_splitter.addWidget(self.frames["QtAxialOrthoViewer"])

        self.frame_3.layout().addWidget(horizontal_splitter)
        self.frame_3.layout().update()
        self.open_data()

    def display_three_images_inverted_t(self):
        self.clear_layout()
        vertical_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        horizontal_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        self.frames["QtSagittalOrthoViewer"].setVisible(True)
        self.frames["QtAxialOrthoViewer"].setVisible(True)
        self.frames["QtCoronalOrthoViewer"].setVisible(True)

        vertical_splitter.addWidget(self.frames["QtSagittalOrthoViewer"])
        vertical_splitter.addWidget(self.frames["QtCoronalOrthoViewer"])
        horizontal_splitter.addWidget(self.frames["QtAxialOrthoViewer"])
        horizontal_splitter.addWidget(vertical_splitter)

        self.frame_3.layout().addWidget(horizontal_splitter)
        self.frame_3.layout().update()
        self.open_data()

    def display_four_images(self):
        """Muestra cuatro visualizadores en una disposición de 2x2."""
        self.clear_layout()
        left_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        right_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        main_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        self.frames["QtSagittalOrthoViewer"].setVisible(True)
        self.frames["QtAxialOrthoViewer"].setVisible(True)
        self.frames["QtCoronalOrthoViewer"].setVisible(True)
        self.frames["QtSegmentationViewer"].setVisible(True)

        left_splitter.addWidget(self.frames["QtSagittalOrthoViewer"])
        left_splitter.addWidget(self.frames["QtAxialOrthoViewer"])
        right_splitter.addWidget(self.frames["QtCoronalOrthoViewer"])
        right_splitter.addWidget(self.frames["QtSegmentationViewer"])
        main_splitter.addWidget(left_splitter)
        main_splitter.addWidget(right_splitter)

        self.frame_3.layout().addWidget(main_splitter)
        self.frame_3.layout().update()
        self.open_data()



    def display_view_3D(self):
        self.clear_layout()
        self.structure = self.structure + 1
        if self.structure > 4:
            self.structure = 1
        self.render_3D = MHD_3DRenderer("./Data/raw/patient.mhd",self.structure)
        self.render_3D.render_mhd_structure(self.structure)

    def open_data(self):
        # Mapeo de estudios
        study_paths = {
        "CT": "CT",  # TAC
        "MR": "MR"   # Resonancia Magnética
        }

        if config.current_patient is None or config.current_study is None:
            QtWidgets.QMessageBox.critical(self.frame_3, "Error", f"Se generó una excepción cargando las imágenes \n {e}")
            return

        # Definir los paths dinámicos basados en el paciente y el estudio
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.join(current_dir, '..')
        base_path = "model/local_database"
        path = os.path.join(project_dir, base_path)
        base_path = f'{path}/{config.current_patient}/{study_paths.get(config.current_study, "CT")}'
        
        # Asigna las rutas para los estudios CT y RM basados en el paciente actual
        file_paths = f'{path}/{config.current_patient}/CT'
        file_paths_2 = f'{path}/{config.current_patient}/MR'

        if config.current_study == 'CT' or config.current_study == 'MR':
            try: 
                self.dcm_viewer.load_dicom_files(base_path)
            except Exception as e:
                print(e)
        else:
            try:
                # Abrir diálogo de carga
                dialog, ui = self.abrir_dialogo_carga()
                # Hacer el diálogo modal
                dialog.setModal(True)
                # Quitar el botón de cerrar
                dialog.setWindowFlags(QtCore.Qt.Window | 
                                    QtCore.Qt.WindowTitleHint | 
                                    QtCore.Qt.CustomizeWindowHint)
                
                # Mostrar el diálogo
                dialog.show()
                # Forzar la actualización de la interfaz
                QtWidgets.QApplication.processEvents()

                # Crear y configurar el hilo de procesamiento
                self.processing_thread = ImageProcessingThread(file_paths, file_paths_2)
                
                # Conectar las señales
                self.processing_thread.finished.connect(
                    lambda file_path: self.processing_finished(file_path, dialog)
                )
                self.processing_thread.error.connect(
                    lambda error: self.processing_error(error, dialog)
                )
                
                # Iniciar el procesamiento
                self.processing_thread.start()

            except Exception as e:
                if dialog:
                    dialog.close()
                print(e)
                QtWidgets.QMessageBox.critical(self.frame_3, "Error", 
                    f"Se generó una excepción cargando las imágenes \n {e}")
                

    def processing_finished(self, file_path, dialog):
        """Maneja la finalización exitosa del procesamiento"""
        try:
            self.load_data(file_path)
            dialog.close()
            self.render_data()
        except Exception as e:
            self.processing_error(str(e), dialog)

    def processing_error(self, error_message, dialog):
        """Maneja los errores durante el procesamiento"""
        if dialog:
            dialog.close()
        print(error_message)
        QtWidgets.QMessageBox.critical(self.frame_3, "Error", 
            f"Se generó una excepción cargando las imágenes \n {error_message}")

    def load_data(self, filename):
        self.vtkBaseClass.connect_on_data(filename)
        self.QtAxialOrthoViewer.connect_on_data(filename)
        self.QtCoronalOrthoViewer.connect_on_data(filename)
        self.QtSagittalOrthoViewer.connect_on_data(filename)
        self.QtSegmentationViewer.connect_on_data(filename)
        self.ViewersConnection.connect_on_data()


    # Render the data   
    def render_data(self):
        self.QtAxialOrthoViewer.render()
        self.QtCoronalOrthoViewer.render()
        self.QtSagittalOrthoViewer.render()
        self.QtSegmentationViewer.render()

    def activate_distance_measurement(self):
        if config.current_study == "CT" or config.current_study == "MR":
            self.dcm_viewer.set_distance_measurement()
        else:
            for view in self.views:
                view.set_distance_measurement("./Data/raw/patient.mhd")

    def set_canvas(self):
        if config.current_study == "CT" or config.current_study == "MR":
            self.dcm_viewer.set_canvas()
        else:
            for view in self.views:
                view.set_canvas()
        
    def clear_canvas_drawing(self):
        if config.current_study == "CT" or config.current_study == "MR":
            self.dcm_viewer.clear_canvas_drawing()
        else:
            for view in self.views:
                view.clear_canvas_drawing()
        
    def set_shape_canvas(self, shape):
        if config.current_study == "CT" or config.current_study == "MR":
            self.dcm_viewer.set_shape_canvas(shape)
        else:
           for view in self.views:
                view.set_shape_canvas(shape)

    def set_text_canvas(self):
        if config.current_study == "CT" or config.current_study == "MR":
            self.dcm_viewer.set_text_canvas()
        else:
            for view in self.views:
                view.set_text_canvas()

    def set_angle_canvas(self):
        if config.current_study == "CT" or config.current_study == "MR":
            self.dcm_viewer.set_angle_canvas()
        else:
            for view in self.views:
                view.set_angle_canvas()

    def clear_tools(self):
        if config.current_study == "CT" or config.current_study == "MR":
            self.dcm_viewer.clear_tools()
        else:
            for view in self.views:
                view.clear_tools()

    def abrir_dialogo_carga(self):
        dialog = QtWidgets.QDialog()
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
        
