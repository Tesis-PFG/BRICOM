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


class ViewerActions:
    def __init__(self, frame_3, dcm_viewer, viewers, ViewersConnection, vtkBaseClass):
        self.frame_3 = frame_3
        self.dcm_viewer = dcm_viewer
        self.QtSagittalOrthoViewer, self.QtAxialOrthoViewer, self.QtCoronalOrthoViewer, self.QtSegmentationViewer = viewers
        self.ViewersConnection = ViewersConnection
        self.vtkBaseClass = vtkBaseClass
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
        self.render_3D = MHD_3DRenderer("./Data/raw/patient.mhd",2)
        self.render_3D.render_mhd_structure(3)

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
                registro(file_paths, file_paths_2)
                # Ruta de la imagen principal (ajusta si cambia según el paciente)
                myFile = f'./Data/raw/patient.mhd'
                # Carga y renderiza los datos
                self.load_data(myFile)
                self.render_data()
            except Exception as e:
                print(e)
                QtWidgets.QMessageBox.critical(self.frame_3, "Error", f"Se generó una excepción cargando las imágenes \n {e}")

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