from PyQt5 import QtWidgets, QtCore
from app.interface.QtOrthoViewer import *
from app.interface.QtSegmentationViewer import *
from app.interface.VtkBase import *
from app.interface.ViewersConnection import *
#Metodo para crear el registro de las imagenes 
from app.interface.mat_3d import registro
from Dicom_vis.DicomViewer import *
import config

class ViewerActions:
    def __init__(self, frame_3, dcm_viewer, viewers, ViewersConnection,vtkBaseClass):
        self.frame_3 = frame_3
        self.dcm_viewer = dcm_viewer
        self.QtSagittalOrthoViewer, self.QtAxialOrthoViewer, self.QtCoronalOrthoViewer, self.QtSegmentationViewer = viewers
        self.ViewersConnection = ViewersConnection
        self.vtkBaseClass = vtkBaseClass

    def clear_layout(self):
        if self.frame_3.layout() is not None:
            while self.frame_3.layout().count():
                child = self.frame_3.layout().takeAt(0)
                if child.widget() and type(child.widget()) == 'QSplitter':
                    self.frame_3.layout().removeWidget(child.widget())


    def display_one_image(self):

        if config.current_study == 'CT' or config.current_study == 'RM':
            self.clear_layout()
            self.dcm_viewer.setFixedSize(500, 500)
            self.QtSagittalOrthoViewer.setFixedSize(0, 0)
            self.QtAxialOrthoViewer.setFixedSize(0, 0)
            self.QtCoronalOrthoViewer.setFixedSize(0, 0)
            self.QtSegmentationViewer.setFixedSize(0, 0)
            self.frame_3.layout().addWidget(self.dcm_viewer)
           
        elif config.current_study == 'ImagenConjunta':
            self.clear_layout()
            self.dcm_viewer.setFixedSize(0, 0)
            self.QtSagittalOrthoViewer.setFixedSize(300, 300)
            self.QtAxialOrthoViewer.setFixedSize(0, 0)
            self.QtCoronalOrthoViewer.setFixedSize(0, 0)
            self.QtSegmentationViewer.setFixedSize(0, 0)
            self.frame_3.layout().addWidget(self.QtSagittalOrthoViewer)

        self.frame_3.layout().update()
        self.frame_3.update()
        self.open_data()


    def display_two_images_vertical(self):
        self.clear_layout()
        self.dcm_viewer.setFixedSize(0, 0)
        self.QtSagittalOrthoViewer.setFixedSize(300, 300)
        self.QtAxialOrthoViewer.setFixedSize(300, 300)
        self.QtCoronalOrthoViewer.setFixedSize(0, 0)
        self.QtSegmentationViewer.setFixedSize(0, 0)
        vertical_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        vertical_splitter.addWidget(self.QtSagittalOrthoViewer)
        vertical_splitter.addWidget(self.QtAxialOrthoViewer)
        self.frame_3.layout().addWidget(vertical_splitter)
        self.frame_3.layout().update()
        self.open_data()


    def display_two_images_horizontal(self):
        self.clear_layout()
        self.dcm_viewer.setFixedSize(0, 0)
        self.QtSagittalOrthoViewer.setFixedSize(300, 300)
        self.QtAxialOrthoViewer.setFixedSize(300, 300)
        self.QtCoronalOrthoViewer.setFixedSize(0, 0)
        self.QtSegmentationViewer.setFixedSize(0, 0)
        horizontal_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        horizontal_splitter.addWidget(self.QtSagittalOrthoViewer)
        horizontal_splitter.addWidget(self.QtAxialOrthoViewer)
        self.frame_3.layout().addWidget(horizontal_splitter)
        self.frame_3.layout().update()
        self.open_data()


    def display_three_images_horizontal(self):
        self.clear_layout()
        self.dcm_viewer.setFixedSize(0, 0)
        self.QtSagittalOrthoViewer.setFixedSize(300, 300)
        self.QtAxialOrthoViewer.setFixedSize(300, 300)
        self.QtCoronalOrthoViewer.setFixedSize(300, 300)
        self.QtSegmentationViewer.setFixedSize(0, 0)
        horizontal_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        horizontal_splitter.addWidget(self.QtSagittalOrthoViewer)
        horizontal_splitter.addWidget(self.QtAxialOrthoViewer)
        horizontal_splitter.addWidget(self.QtCoronalOrthoViewer)
        self.frame_3.layout().addWidget(horizontal_splitter)
        self.frame_3.layout().update()
        self.open_data()


    def display_three_images_t(self):
        self.clear_layout()
        self.dcm_viewer.setFixedSize(0, 0)
        self.QtSagittalOrthoViewer.setFixedSize(300, 300)
        self.QtAxialOrthoViewer.setFixedSize(300, 300)
        self.QtCoronalOrthoViewer.setFixedSize(300, 300)
        self.QtSegmentationViewer.setFixedSize(0, 0)
        vertical_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        vertical_splitter.addWidget(self.QtSagittalOrthoViewer)
        vertical_splitter.addWidget(self.QtCoronalOrthoViewer)
        horizontal_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        horizontal_splitter.addWidget(vertical_splitter)
        horizontal_splitter.addWidget(self.QtAxialOrthoViewer)
        self.frame_3.layout().addWidget(horizontal_splitter)
        self.frame_3.layout().update()
        self.open_data()


    def display_three_images_inverted_t(self):
        self.clear_layout()
        self.dcm_viewer.setFixedSize(0, 0)
        self.QtSagittalOrthoViewer.setFixedSize(300, 300)
        self.QtAxialOrthoViewer.setFixedSize(300, 300)
        self.QtCoronalOrthoViewer.setFixedSize(300, 300)
        self.QtSegmentationViewer.setFixedSize(0, 0)
        vertical_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        vertical_splitter.addWidget(self.QtSagittalOrthoViewer)
        vertical_splitter.addWidget(self.QtCoronalOrthoViewer)
        horizontal_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        horizontal_splitter.addWidget(self.QtAxialOrthoViewer)
        horizontal_splitter.addWidget(vertical_splitter)
        self.frame_3.layout().addWidget(horizontal_splitter)
        self.frame_3.layout().update()
        self.open_data()


    def display_four_images(self):
        self.clear_layout()
        self.dcm_viewer.setFixedSize(0, 0)
        self.QtSagittalOrthoViewer.setFixedSize(300, 300)
        self.QtAxialOrthoViewer.setFixedSize(300, 300)
        self.QtCoronalOrthoViewer.setFixedSize(300, 300)
        self.QtSegmentationViewer.setFixedSize(300, 300)
        left_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        left_splitter.addWidget(self.QtSagittalOrthoViewer)
        left_splitter.addWidget(self.QtAxialOrthoViewer)
        right_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        right_splitter.addWidget(self.QtCoronalOrthoViewer)
        right_splitter.addWidget(self.QtSegmentationViewer)
        main_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        main_splitter.addWidget(left_splitter)
        main_splitter.addWidget(right_splitter)
        self.frame_3.layout().addWidget(main_splitter)
        self.frame_3.layout().update()
        self.open_data()


    def open_data(self):
        # Mapeo de estudios
        study_paths = {
        "CT": "CT",  # TAC
        "RM": "RM"   # Resonancia Magnética
        }

        if config.current_patient is None or config.current_study is None:
            QtWidgets.QMessageBox.critical(self, "Error", "No hay un paciente o estudio seleccionado.")
            return

        # Definir los paths dinámicos basados en el paciente y el estudio
        base_path = f'./local_database/{config.current_patient}/{study_paths.get(config.current_study, "CT")}/'
        
        # Asigna las rutas para los estudios CT y RM basados en el paciente actual
        file_paths = f'./local_database/{config.current_patient}/CT'
        file_paths_2 = f'./local_database/{config.current_patient}/MR'

        if config.current_study == 'CT' or config.current_study == 'MR':
            try: 
                self.dcm_viewer.load_dicom_files(base_path)
            except Exception as e:
                print(e)
                QtWidgets.QMessageBox.critical(self, "Error", f"Se generó una excepción cargando las imágenes \n {e}")
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
                QtWidgets.QMessageBox.critical(self, "Error", f"Se generó una excepción cargando las imágenes \n {e}")

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
