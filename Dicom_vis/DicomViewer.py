from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import vtk
import os
import pydicom
from vtkmodules.util import numpy_support
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class DicomViewer(QWidget):
    
    # Constructor
    def __init__(self, dicom_folder_path, label: str = "DICOM Viewer"):
        super(DicomViewer, self).__init__()
        
        self.dicom_folder_path = dicom_folder_path
        self.label = label
        self.status = False
        
        self.dicom_files = self.load_dicom_files(self.dicom_folder_path)
        self.min_slice = 0
        self.max_slice = len(self.dicom_files) - 1
        self.current_slice = self.min_slice
        
        self.vtkWidget = QVTKRenderWindowInteractor(self)
        self.viewer = vtk.vtkImageViewer2()
        self.viewer.SetRenderWindow(self.vtkWidget.GetRenderWindow())
        self.viewer.SetupInteractor(self.vtkWidget.GetRenderWindow().GetInteractor())  
        
        self._init_UI()
        self.update_slice(self.current_slice)

    def load_dicom_files(self, folder_path):
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"El folder al que se quiere acceder no existe: {folder_path}")
        dicom_files = []
        for filename in os.listdir(folder_path):
            if filename.endswith('.dcm'):
                dicom_files.append(os.path.join(folder_path, filename))
        return dicom_files


    # Initialize the UI
    def _init_UI(self):
        # Layout principal
        main_layout = QVBoxLayout(self)
        color_light = "#E2BBE9" 
        color_dark = "#5A639C"

        # Layout horizontal para imagen y slider
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
        
        # Añadir el widget de imagen y el slider al layout horizontal
        image_slider_layout.addWidget(self.vtkWidget)  # Añadir el visualizador de imagen
        image_slider_layout.addWidget(self.slider)     # Añadir el slider a la derecha
        
        # Añadir el layout de imagen+slider al layout principal
        main_layout.addLayout(image_slider_layout)
        
        # Layout horizontal para los botones
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
        
        # Añadir los botones al layout de botones
        self.buttonsLayout.addWidget(self.prevBtn)
        self.buttonsLayout.addWidget(self.playBtn)
        self.buttonsLayout.addWidget(self.nextBtn)
        
        # Añadir el layout de botones al layout principal, justo debajo de la imagen
        main_layout.addLayout(self.buttonsLayout)
        self.prevBtn.clicked.connect(lambda: self.next_prev_btn(self.slider.value()-10))
        self.playBtn.clicked.connect(self.play_pause_btn)
        self.nextBtn.clicked.connect(lambda: self.next_prev_btn(self.slider.value()+10))


    def update_slice(self, slice_index):
        if slice_index < self.min_slice:
            slice_index = self.min_slice
        elif slice_index > self.max_slice:
            slice_index = self.max_slice
        self.current_slice = slice_index
        
        dicom_data = pydicom.dcmread(self.dicom_files[slice_index])
        pixel_array = dicom_data.pixel_array
        
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


    def next_prev_btn(self, slice_index):
        # Asegúrate de que el índice no exceda los límites
        if slice_index < self.slider.minimum():
            slice_index = self.slider.minimum()
        elif slice_index > self.slider.maximum():
            slice_index = self.slider.maximum()

        # Establecer el valor del slider al nuevo índice de corte
        self.slider.setValue(slice_index)

        # Actualizar el visualizador con el nuevo slice
        self.update_slice(slice_index)

    
    # Función de play y pausa  
    def play_pause_btn(self):
        pass
