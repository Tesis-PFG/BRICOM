from PyQt5 import QtWidgets, QtCore
from app.interface.QtOrthoViewer import *
from app.interface.QtSegmentationViewer import *
from app.interface.VtkBase import *
from app.interface.ViewersConnection import *
#Metodo para crear el registro de las imagenes 
from app.interface.mat_3d import registro
from Dicom_vis.DicomViewer import *
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QPoint
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

    def activate_distance_measurement(self,measurement_view):
                if measurement_view is None:
                        # Crear la instancia de medición
                        measurement_view = DistanceMeasurement("./app/tmp/out.mhd",self.QtSagittalOrthoViewer.get_viewer())
                        # Mostrar la vista
                        measurement_view.show()
                else:
                        measurement_view.close()
                        measurement_view = None 
            
    def set_canvas(self, canvas):
            if canvas is None:
                    # Crear una instancia del canvas como hijo de frame_3
                    canvas = Canvas(self.QtSagittalOrthoViewer.get_viewer())
                    # Asegurarse de que el canvas no interfiera con el widget subyacente
                    # self.canvas.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
                    # Mostrar el canvas
                    canvas.show()

            else:
                    canvas.close()
                    canvas = None


# Clase para dibujar
class Canvas(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)
        # Enable mouse tracking for the widget
        self.setMouseTracking(True)
        
        # Set size of the canvas
        self.setFixedSize(parent.size())
        
        # Enable transparent background for the widget itself
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)

        # Create a transparent pixmap
        pixmap = QtGui.QPixmap(self.size())
        pixmap.fill(QtGui.QColor(0, 0, 0, 0))  # Fully transparent background
        self.setPixmap(pixmap)

        self.last_x, self.last_y = None, None
        self.pen_color = QtGui.QColor('#ff0000')
        
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.eraseRect(self.rect())
        
        # Ensure transparency by setting the composition mode
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        
        # This prevents any automatic background fill, keeping the canvas transparent
        super().paintEvent(event)  # Call the base class's paint event if needed

    def mouseMoveEvent(self, e):
        if self.last_x is None:  # First event.
            self.last_x = e.x()
            self.last_y = e.y()
            return  # Ignore the first time.

        # Check if we are inside the drawing area
        if e.buttons() == QtCore.Qt.LeftButton:
            painter = QtGui.QPainter(self.pixmap())
            pen = QtGui.QPen(self.pen_color, 4)
            painter.setPen(pen)
            painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
            painter.end()
            self.update()

        # Update the origin for next time.
        self.last_x = e.x()
        self.last_y = e.y()

    def mousePressEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.last_x = e.x()
            self.last_y = e.y()

    def mouseReleaseEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.last_x = None
            self.last_y = None


class DistanceMeasurement(QWidget):
    def __init__(self, mhd_file, parent=None):
        super().__init__(parent)
        self.start_point = None
        self.end_point = None
        self.is_measuring = False
        self.pixel_spacing = self.extract_pixel_spacing(mhd_file)  # Extrae el tamaño de los píxeles
        
        # Set size of the canvas
        self.setFixedSize(parent.size())
        
        # Enable transparent background for the widget itself
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)

    def extract_pixel_spacing(self, mhd_file):
        """Lee el archivo .mhd y extrae el tamaño de los píxeles."""
        with open(mhd_file, 'r') as file:
            for line in file:
                if line.startswith("ElementSpacing"):
                    # Formato típico: ElementSpacing = x_spacing y_spacing z_spacing
                    spacing = line.split('=')[1].strip().split()
                    # Nos interesa solo el tamaño en 2D, así que tomamos x_spacing y y_spacing
                    x_spacing = float(spacing[0])
                    y_spacing = float(spacing[1])
                    # Suponiendo que queremos la media de los valores de x e y
                    return (x_spacing + y_spacing) / 2
        return 1.0  # Valor predeterminado si no se encuentra ElementSpacing

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if not self.is_measuring:
                # Primer clic, marca el punto de inicio
                self.start_point = event.pos()
                self.end_point = None  # Resetea el punto final
                self.is_measuring = True
                self.update()  # Borra cualquier medición anterior
            else:
                # Segundo clic, marca el punto final
                self.end_point = event.pos()
                self.is_measuring = False
                self.update()  # Solicita una actualización de la pantalla para dibujar la línea final

    def paintEvent(self, event):
        # Limpia la pantalla antes de realizar una nueva medición
        painter = QPainter(self)
        painter.eraseRect(self.rect())  # Borra el contenido anterior
        
        if self.start_point and self.end_point:
            painter.setRenderHint(QPainter.Antialiasing)
            pen = QPen(Qt.red, 2)
            painter.setPen(pen)
            painter.drawLine(self.start_point, self.end_point)

            # Calcula la distancia en píxeles y convierte a milímetros
            distance_pixels = self.calculate_distance(self.start_point, self.end_point)
            distance_mm = distance_pixels * self.pixel_spacing

            # Muestra la distancia en pantalla
            painter.drawText(self.end_point, f"{distance_mm:.2f} mm")

    def calculate_distance(self, point1, point2):
        # Calcula la distancia euclidiana entre dos puntos
        return ((point2.x() - point1.x())**2 + (point2.y() - point1.y())**2)**0.5
