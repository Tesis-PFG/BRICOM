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
from config import current_patient, all_patients, current_study 


class DicomViewer(QWidget):

    def __init__(self, view_orientation='Axial'):
        super(DicomViewer, self).__init__()

        self.view_orientation = view_orientation
        self.status = False
        self.max_slice = 0
        self.dicom_files = None
        self.min_slice = 0
        
        self.current_slice = self.min_slice
        
        # Brillo y contraste por defecto
        self.brightness = 0  # Valor de brillo
        self.contrast = 1.0  # Valor de contraste normalizado entre 0 y 2
        
        self.vtkWidget = QVTKRenderWindowInteractor(self)
        self.viewer = vtk.vtkResliceImageViewer()
        self.viewer.SetRenderWindow(self.vtkWidget.GetRenderWindow())
        self.viewer.SetupInteractor(self.vtkWidget.GetRenderWindow().GetInteractor())
        
        self._init_UI()
        self.set_view_orientation(self.view_orientation)

       

    def load_dicom_files(self, folder_path):
        dicom_files = []
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"El folder al que se quiere acceder no existe: {folder_path}")
        for filename in os.listdir(folder_path):
            if filename.endswith('.dcm'):
                dicom_files.append(os.path.join(folder_path, filename))
        self.max_slice = len(dicom_files) - 1
        self.dicom_files = dicom_files
        self.slider.setMaximum(self.max_slice)  # Actualizar el rango máximo del slider
         # Mostrar metadata en la esquina superior izquierda
        self.show_patient_metadata()
        self.update_slice(self.current_slice)

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

        # Añadir QLabel y Slider para brillo y contraste
        self.contrast_label = QLabel(f'Contraste: {self.contrast:.2f}')
        self.contrast_label.setStyleSheet("""
            color: #ffffff;
        """)

        # Añadir QLabel y Slider para brillo
        self.brightness_label = QLabel(f'Brillo: {self.brightness:.2f}')
        self.brightness_label.setStyleSheet("color: #ffffff;")

        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #ffffff;
                width: 500px;
                height: 10px;                           
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #5A639C;
                border: 1px solid #5c5c5c;
                width: 50px;
                height: 10px;  
                margin: -5px 0; 
                border-radius: 100px; 
            }
        """)
        self.brightness_slider.setRange(-100, 100)  # Rango de -100 a 100 para el brillo
        self.brightness_slider.setValue(0)           # Valor por defecto al 0%
        self.brightness_slider.valueChanged.connect(self.update_brightness)

        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #ffffff;
                width: 500px;
                height : 10px;                           
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #5A639C;
                border: 1px solid #5c5c5c;
                width: 50px;
                height: 10px;  
                margin: -5px 0; 
                border-radius: 100px; 
            }
        """)
        self.contrast_slider.setRange(50, 200)  # Rango de 50 a 200 para evitar 0
        self.contrast_slider.setValue(100)      # Valor por defecto al 100%
        self.contrast_slider.valueChanged.connect(self.update_contrast)

        # Añadir QLabel y Slider al layout
        main_layout.addWidget(self.brightness_label)
        main_layout.addWidget(self.brightness_slider)
        main_layout.addWidget(self.contrast_label)
        main_layout.addWidget(self.contrast_slider)

        self.setLayout(main_layout)

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
        elif view == 'Sagittal':
            self.viewer.SetSliceOrientationToYZ()
        elif view == 'Coronal':
            self.viewer.SetSliceOrientationToXZ()
        else:
            raise ValueError("La vista proporcionada no es válida. Usa 'Axial', 'Sagittal' o 'Coronal'.")
        
        self.viewer.Render()

    def update_slice(self, slice_index):
        if slice_index < self.min_slice:
            slice_index = self.min_slice
        elif slice_index > self.max_slice:
            slice_index = self.max_slice
        self.current_slice = slice_index
        
        dicom_data = pydicom.dcmread(self.dicom_files[slice_index])
        pixel_array = dicom_data.pixel_array
        
        # Ajustar brillo y contraste
        pixel_array = self.adjust_brightness_contrast(pixel_array)

        vtk_data_array = numpy_support.numpy_to_vtk(pixel_array.ravel(), deep=True, array_type=vtk.VTK_FLOAT)
        vtk_image = vtk.vtkImageData()

        if pixel_array.ndim == 2:
            vtk_image.SetDimensions(pixel_array.shape[1], pixel_array.shape[0], 1)
        elif pixel_array.ndim == 3:
            vtk_image.SetDimensions(pixel_array.shape[2], pixel_array.shape[1], pixel_array.shape[0])
        else:
            raise ValueError("Forma de array sin soporte: {}".format(pixel_array.shape))
            
        vtk_image.GetPointData().SetScalars(vtk_data_array)
        self.viewer.SetInputData(vtk_image)
        self.viewer.Render()

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
        patient = None
        # print(f'El paciente que se busca es: {current_patient}')
        # TODO: Hablar con moises, la variable current_patient no se esta almacenando de manera correcta 
        for p in all_patients:
            if p[0] == current_patient: 
                patient = p
                break

        # Comprobar si se encontró el paciente
        if patient is not None:
            # Crear un QLabel para mostrar el nombre y apellido del paciente
            #Revisar si la extracciòn de datos es correcta de acuerdo a como se almacenan en datos
            self.metadata_label = QLabel(f"Paciente: {patient['last_name']} {patient['first_name']}", self)
        else:
            self.metadata_label = QLabel(f"No hay informaciòn del paciente {current_patient}", self)
            print("No se encontró información del paciente.")

        self.metadata_label.setStyleSheet("""
                color: white;
                background-color: rgba(0, 0, 0, 50%);
                font-size: 14px;
                padding: 5px;
            """)
        self.metadata_label.setFixedWidth(250)
        self.metadata_label.setFixedHeight(30)
        self.metadata_label.move(10, 10)  # Posicionar el QLabel en la esquina superior izquierda
        self.metadata_label.show()
