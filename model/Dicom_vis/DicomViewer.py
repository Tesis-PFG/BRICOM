from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import vtk
import os
import pydicom
import numpy as np  # Importa numpy para manejar operaciones numéricas
from vtkmodules.util import numpy_support
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from app.interface.Worker import *
import SimpleITK as sitk
from model.Herramientas import *
import model.config as config


class DicomViewer(QWidget):

    def __init__(self, view_orientation='Axial'):
        super(DicomViewer, self).__init__()

        self.view_orientation = view_orientation
        self.status = False
        self.max_slice = 0
        self.dicom_files = None
        self.min_slice = 0
        self.canvas = None  # Inicializar el Canvas como None
        self.shape_canvas = None # Inicializar
        self.distance_measurement = None  # Inicializar DistanceMeasurement como None
        self.text_canvas = None # Inicializar TextCanvas como None
        self.angle_canvas = None # Inicializar AngleMeasurement como None
        self.current_slice = self.min_slice
        
        # Brillo y contraste por defecto
        self.brightness = 0  # Valor de brillo
        self.contrast = 1.0  # Valor de contraste normalizado entre 0 y 2
        
        self.vtkWidget = QVTKRenderWindowInteractor(self)
        self.viewer = vtk.vtkImageViewer2()        
        self.viewer.SetRenderWindow(self.vtkWidget.GetRenderWindow())
        self.viewer.SetupInteractor(self.vtkWidget.GetRenderWindow().GetInteractor())
        
        self._init_UI()
        self.set_view_orientation(self.view_orientation)


    def _init_UI(self):
        main_layout = QVBoxLayout(self)
        color_light = "#E2BBE9" 
        color_dark = "#5A639C"

        # Layout para el slider y la imagen
        image_slider_layout = QHBoxLayout()

        # Slider
        self.slider = QSlider(Qt.Vertical)
        self.slider.setMinimum(self.min_slice)
        self.slider.setMaximum(self.max_slice)
        self.slider.setSingleStep(1)
        self.slider.setValue(0)
        self.slider.setEnabled(True)
        self.slider.valueChanged.connect(self.update_slice)

        self.slider.setStyleSheet("""
            QSlider::groove:vertical {
                background: #ffffff;
                width: 10px;
                border-radius: 4px;
            }
            QSlider::handle:vertical {
                background: #5A639C;
                border: 1px solid #5c5c5c;
                height: 25px;  
                margin: -5px 0; 
                border-radius: 100px; 
            }
        """)
        
        # Añadir el widget de imagen y el slider al layout
        image_slider_layout.addWidget(self.vtkWidget)
        image_slider_layout.addWidget(self.slider)
        
        main_layout.addLayout(image_slider_layout)

        # Layout para los botones
        self.buttonsLayout = QHBoxLayout()
        
        self.prevBtn = QPushButton()
        self.prevBtn.setIcon(QIcon("./app/assets/decrease.svg"))
        self.prevBtn.setStyleSheet(f"font-size:15px; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px; background: {color_light}")

        self.playBtn = QPushButton()
        self.playBtn.setIcon(QIcon("./app/assets/play.ico"))
        self.playBtn.setStyleSheet(f"font-size:15px; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px; background: {color_dark}")

        self.nextBtn = QPushButton()
        self.nextBtn.setIcon(QIcon("./app/assets/increase.svg"))
        self.nextBtn.setStyleSheet(f"font-size:15px; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px; background: {color_light}")

        self.buttonsLayout.setSpacing(10)
        self.buttonsLayout.addWidget(self.prevBtn)
        self.buttonsLayout.addWidget(self.playBtn)
        self.buttonsLayout.addWidget(self.nextBtn)

        main_layout.addLayout(self.buttonsLayout)
        self.prevBtn.clicked.connect(lambda: self.next_prev_btn(self.slider.value()-10))
        self.playBtn.clicked.connect(self.play_pause_btn)
        self.nextBtn.clicked.connect(lambda: self.next_prev_btn(self.slider.value()+10))

        self.setLayout(main_layout)
    
    def load_dicom_files(self, folder_path):
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"El folder al que se quiere acceder no existe: {folder_path}")

        # Usar VTK DICOM Image Reader
        self.reader = vtk.vtkDICOMImageReader()
        self.reader.SetDirectoryName(folder_path)
        self.reader.Update()

        # Obtener el número de slices
        vtk_image = self.reader.GetOutput()
        
        # Comprobar si vtk_image es None
        if vtk_image is None:
            raise ValueError("No se pudo leer la imagen DICOM. vtk_image es None.")

        ct_dimensions = vtk_image.GetDimensions()
        
        # Comprobar si las dimensiones son válidas
        if ct_dimensions is None or len(ct_dimensions) < 3:
            raise ValueError("Las dimensiones de la imagen DICOM son inválidas.")

        self.max_slice = ct_dimensions[2] - 1  # Dimensiones son en el orden (X, Y, Z)
        if self.max_slice < 1:
            raise ValueError("No hay suficientes imágenes DICOM para visualizar.")

        # Verificar que self.slider esté inicializado y sea del tipo adecuado
        if hasattr(self, 'slider') and isinstance(self.slider, QSlider):
            try:
                self.slider.setMaximum(self.max_slice)
            except Exception as e:
                print(f"Error actualizando el slider: {e}")
        else:
            print("El slider no está inicializado correctamente.")

        # Mostrar metadata en la esquina superior izquierda
        self.show_patient_metadata()

        # Extraer el Pixel Spacing (tamaño de los píxeles en mm)
        self.pixel_spacing = self.get_pixel_spacing()

        # Actualizar el primer slice
        self.update_slice(0)


    def update_brightness(self, value):
        self.brightness = value
        self.brightness_label.setText(f'Brillo: {self.brightness:.2f}')  # Actualizar el QLabel
        self.update_slice(self.current_slice)  # Volver a renderizar la imagen con el nuevo brillo


    def update_contrast(self, value):
        self.contrast = value / 100.0  # Normalizar contraste al rango [0.5, 2.0]
        self.contrast_label.setText(f'Contraste: {self.contrast:.2f}')  # Actualizar el QLabel
        self.update_slice(self.current_slice)  # Volver a renderizar la imagen con el nuevo contraste


    def set_view_orientation(self, view):
        if view == 'Axial':
            self.viewer.SetSliceOrientationToXY()
            self.viewer.GetRenderer().GetActiveCamera().Roll(180)  # Rueda la cámara 180 grados

        elif view == 'Sagittal':
            self.viewer.SetSliceOrientationToYZ()
            self.viewer.GetRenderer().GetActiveCamera().Roll(180)  # Rueda la cámara 180 grados
        elif view == 'Coronal':
            self.viewer.SetSliceOrientationToXZ()
            self.viewer.GetRenderer().GetActiveCamera().Roll(180)  # Rueda la cámara 180 grados

        else:
            raise ValueError("La vista proporcionada no es válida. Usa 'Axial', 'Sagittal' o 'Coronal'.")
        self.viewer.Render()


    def update_slice(self, slice_index):
        if slice_index < 0:
            slice_index = 0
        elif slice_index > self.max_slice:
            slice_index = self.max_slice
        self.current_slice = slice_index

        # Leer la imagen DICOM desde el reader
        vtk_image = self.reader.GetOutput()

        # Verificar si la imagen contiene datos de píxeles
        if vtk_image.GetPointData().GetScalars() is None:
            print(f"La imagen en la posición {slice_index} no contiene datos de píxeles, se omitirá.")
            return

        # Establecer el slice en el viewer
        self.viewer.SetInputData(vtk_image)
        self.viewer.SetSlice(slice_index)

        # Restablecer la cámara para encuadrar la imagen actual
        self.viewer.GetRenderer().ResetCamera() 
        # Actualizar la visualización
        self.viewer.Render()
        # Ajustar la cámara al nuevo slice
        self.vtkWidget.GetRenderWindow().Render()  # Renderizar el widget

    def adjust_brightness_contrast(self, image):
        image = image.astype(np.float32)
        adjusted_image = self.contrast * (image - 127.5) + 127.5 + self.brightness
        adjusted_image = np.clip(adjusted_image, 0, 255)
        return adjusted_image
    

    def next_prev_btn(self, slice_index):
        if slice_index < self.slider.minimum():
            slice_index = self.slider.minimum()
        elif slice_index > self.slider.maximum():
            slice_index = self.slider.maximum()

        self.slider.setValue(slice_index)
        self.update_slice(slice_index)


    def play_slices(self):
        self.thread = QThread()
        self.worker = Worker(self.slider)
        self.status = True  
        self.playBtn.setIcon(QIcon("./app/assets/pause.ico"))

        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.play)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.worker.progress.connect(self.update_slice)
        self.thread.start()
        self.slider.setHidden(True)

        self.thread.finished.connect(lambda: self.slider.setHidden(False))
        self.thread.finished.connect(self.pause_slices)


    def pause_slices(self):
        self.playBtn.setIcon(QIcon("./app/assets/play.ico"))
        self.worker.pause()
        self.status = False


    def play_pause_btn(self):
        if self.status is False:
            self.play_slices()
        else:
            self.pause_slices()


    def show_patient_metadata(self):
        # Buscar el paciente actual en la lista de todos los pacientes
        patient_metadata = None 
        print(f"El paciente que se está buscando es {config.current_patient}") 

        if config.current_patient is not None:
            patient_metadata = config.all_patients.get(config.current_patient)
            print(f'{patient_metadata}')

        # Comprobar si se encontró el paciente
        if patient_metadata is not None:
            patient_id = patient_metadata.get('PatientID', 'Desconocido')
            full_name = patient_metadata.get('PatientName', 'Desconocido')
            name_parts = full_name.split()  
            last_name = " ".join(name_parts[:-1])
            first_name = name_parts[-1]           

            study_date = ''
            if patient_metadata.get('modalidades'):
                for modality, study_info in patient_metadata['modalidades'].items():
                    study_date = study_info.get('StudyDate', 'Desconocida')
                    break 
            
            # Verificar si ya existe un QLabel y eliminarlo si es necesario
            if hasattr(self, 'metadata_label'):
                self.metadata_label.deleteLater()  # Eliminar el QLabel anterior

            # Crear un nuevo QLabel
            self.metadata_label = QLabel(
                f"ID Paciente: {patient_id}\n{last_name} {first_name}\nFecha de Realización: {study_date}",
                self
            )
        else:
            # Verificar si ya existe un QLabel y eliminarlo si es necesario
            if hasattr(self, 'metadata_label'):
                self.metadata_label.deleteLater()  # Eliminar el QLabel anterior

            self.metadata_label = QLabel(f"No hay información del paciente {config.current_patient}", self)
            print("No se encontró información del paciente.")

        # Configurar propiedades del QLabel
        self.metadata_label.setStyleSheet("""
                color: white;
                background-color: rgba(0, 0, 0, 50%);
                font-size: 14px;
                padding: 5px;
            """)
        self.metadata_label.setFixedWidth(250)
        self.metadata_label.setFixedHeight(60)  # Aumentar la altura para permitir más líneas
        self.metadata_label.move(10, 10)  # Posicionar el QLabel en la esquina superior izquierda
        self.metadata_label.show()

    def get_pixel_spacing(self):
        """Obtiene el tamaño de los píxeles del archivo DICOM en mm."""
        if 'PixelSpacing' in self.dicom_files[3]:
            pixel_spacing = self.dicom_files[3].PixelSpacing  # List [X_spacing, Y_spacing]
            return (float(pixel_spacing[0]) + float(pixel_spacing[1])) / 2  # Tamaño en X y Y
        else:
            # Valor por defecto si no existe el campo PixelSpacing
            return 1.0

    
    # Método para inicializar Canvas
    def set_canvas(self):
        if self.canvas is None:
            # Crear e insertar el Canvas sobre el viewer
            self.canvas = Canvas(self)
            self.canvas.show()

        else:
            # Si ya existe, ocultar el Canvas
            self.canvas.close()
            self.canvas = None

    # Método para inicializar DistanceMeasurement
    def set_distance_measurement(self):
        if self.distance_measurement is None:
            # Crear e insertar DistanceMeasurement
            self.distance_measurement = DistanceMeasurementDicom(1.0, self) #TODO: Fix spacing self.pixel_spacing()
            self.distance_measurement.show()
        else:
            # Si ya existe, ocultar DistanceMeasurement
            self.distance_measurement.close()
            self.distance_measurement = None
            
    # Método para borrar el contenido del Canvas
    def clear_canvas_drawing(self):
        if self.canvas:
            self.canvas.clear_canvas()
        if self.shape_canvas:
            self.shape_canvas.clear_canvas()
        if self.text_canvas:
            self.text_canvas.clear_canvas()
        if self.angle_canvas:
            self.angle_canvas.clear_canvas()

            
    def set_shape_canvas(self, shape):
        if self.shape_canvas is None:
            # Crear e insertar el Canvas sobre el viewer
            self.shape_canvas = ShapeCanvas(self)
            self.shape_canvas.set_shape(shape)
            self.shape_canvas.show()
        else:
            # Si ya existe, ocultar el Canvas
            self.shape_canvas.close()
            self.shape_canvas = None

    def set_text_canvas(self):
        if self.text_canvas is None:
            self.text_canvas = TextCanvas(self)
            self.text_canvas.show()
        else:
            # Si ya existe, ocultar el Canvas
            self.text_canvas.close()
            self.text_canvas = None

    def set_angle_canvas(self):
        if self.angle_canvas is None:
            self.angle_canvas = AngleMeasurement(self)
            self.angle_canvas.show()
        else:
            # Si ya existe, ocultar el Canvas
            self.angle_canvas.close()
            self.angle_canvas = None
