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
        self.views = [self.QtSagittalOrthoViewer, self.QtAxialOrthoViewer, self.QtCoronalOrthoViewer]


    def hide_studies(self):
        self.render_3D.setFixedSize(0, 0)
        self.dcm_viewer.setFixedSize(0, 0)
        self.QtSagittalOrthoViewer.setFixedSize(0, 0)
        self.QtAxialOrthoViewer.setFixedSize(0, 0)
        self.QtCoronalOrthoViewer.setFixedSize(0, 0)
        self.QtSegmentationViewer.setFixedSize(0, 0)
        self.current_splitter = None

    def clear_layout(self):
        if self.current_splitter:
            self.frame_3.layout().removeWidget(self.current_splitter)
            self.current_splitter.deleteLater()
            self.current_splitter = None

    def add_viewer_to_frame(self, parent_splitter, viewer):
        frame = QtWidgets.QFrame()
        frame_layout = QtWidgets.QVBoxLayout()
        frame.setLayout(frame_layout)
        frame_layout.addWidget(viewer)
        parent_splitter.addWidget(frame)


    def display_one_image(self):
        self.clear_layout()
        self.current_splitter = QtWidgets.QSplitter(Qt.Vertical)
        
        frame = QtWidgets.QFrame()
        frame_layout = QtWidgets.QVBoxLayout()
        frame.setLayout(frame_layout)
        
        if config.current_study == 'CT' or config.current_study == 'MR':
            self.dcm_viewer.setFixedSize(500, 500)
            frame_layout.addWidget(self.dcm_viewer)
        elif config.current_study == 'ImagenConjunta':
            self.QtSagittalOrthoViewer.setFixedSize(300, 300)
            frame_layout.addWidget(self.QtSagittalOrthoViewer)

        self.current_splitter.addWidget(frame)
        self.frame_3.layout().addWidget(self.current_splitter)
        self.frame_3.layout().update()
        self.open_data()

    def display_two_images_vertical(self):
        self.clear_layout()
        self.current_splitter = QtWidgets.QSplitter(Qt.Vertical)

        for viewer in [self.QtSagittalOrthoViewer, self.QtAxialOrthoViewer]:
            viewer.setFixedSize(300, 300)
            self.add_viewer_to_frame(self.current_splitter, viewer)

        self.frame_3.layout().addWidget(self.current_splitter)
        self.frame_3.layout().update()
        self.open_data()

    def display_two_images_horizontal(self):
        self.clear_layout()
        self.current_splitter = QtWidgets.QSplitter(Qt.Horizontal)

        for viewer in [self.QtSagittalOrthoViewer, self.QtAxialOrthoViewer]:
            viewer.setFixedSize(300, 300)
            self.add_viewer_to_frame(self.current_splitter, viewer)

        self.frame_3.layout().addWidget(self.current_splitter)
        self.frame_3.layout().update()
        self.open_data()

    def display_three_images_horizontal(self):
        self.clear_layout()
        self.current_splitter = QtWidgets.QSplitter(Qt.Horizontal)

        for viewer in [self.QtSagittalOrthoViewer, self.QtAxialOrthoViewer, self.QtCoronalOrthoViewer]:
            viewer.setFixedSize(300, 300)
            self.add_viewer_to_frame(self.current_splitter, viewer)

        self.frame_3.layout().addWidget(self.current_splitter)
        self.frame_3.layout().update()
        self.open_data()

    def display_three_images_t(self):
        self.clear_layout()
        vertical_splitter = QtWidgets.QSplitter(Qt.Vertical)
        self.current_splitter = QtWidgets.QSplitter(Qt.Horizontal)

        for viewer in [self.QtSagittalOrthoViewer, self.QtCoronalOrthoViewer]:
            viewer.setFixedSize(300, 300)
            self.add_viewer_to_frame(vertical_splitter, viewer)

        self.current_splitter.addWidget(vertical_splitter)
        self.add_viewer_to_frame(self.current_splitter, self.QtAxialOrthoViewer)

        self.frame_3.layout().addWidget(self.current_splitter)
        self.frame_3.layout().update()
        self.open_data()

    def display_three_images_inverted_t(self):
        self.clear_layout()
        vertical_splitter = QtWidgets.QSplitter(Qt.Vertical)
        self.current_splitter = QtWidgets.QSplitter(Qt.Horizontal)

        for viewer in [self.QtSagittalOrthoViewer, self.QtCoronalOrthoViewer]:
            viewer.setFixedSize(300, 300)
            self.add_viewer_to_frame(vertical_splitter, viewer)

        self.current_splitter.addWidget(self.QtAxialOrthoViewer)
        self.current_splitter.addWidget(vertical_splitter)

        self.frame_3.layout().addWidget(self.current_splitter)
        self.frame_3.layout().update()
        self.open_data()

    def display_four_images(self):
        self.clear_layout()
        left_splitter = QtWidgets.QSplitter(Qt.Vertical)
        right_splitter = QtWidgets.QSplitter(Qt.Vertical)
        self.current_splitter = QtWidgets.QSplitter(Qt.Horizontal)

        for viewer in [self.QtSagittalOrthoViewer, self.QtAxialOrthoViewer]:
            viewer.setFixedSize(300, 300)
            self.add_viewer_to_frame(left_splitter, viewer)

        for viewer in [self.QtCoronalOrthoViewer, self.QtSegmentationViewer]:
            viewer.setFixedSize(300, 300)
            self.add_viewer_to_frame(right_splitter, viewer)

        self.current_splitter.addWidget(left_splitter)
        self.current_splitter.addWidget(right_splitter)

        self.frame_3.layout().addWidget(self.current_splitter)
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