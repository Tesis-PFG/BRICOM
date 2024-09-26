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
        # Layouts
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Slider
        self.slider = QSlider(Qt.Vertical)
        self.slider.setMinimum(self.min_slice)
        self.slider.setMaximum(self.max_slice)
        self.slider.setValue(self.current_slice)
        self.slider.valueChanged.connect(self.update_slice)
        
        # Buttons
        self.buttonsLayout = QHBoxLayout()
        self.prevBtn = QPushButton("Prev")
        self.prevBtn.clicked.connect(lambda: self.update_slice(self.current_slice - 1))
        
        self.playBtn = QPushButton("Play")
        self.playBtn.clicked.connect(self.play_pause_btn)
        
        self.nextBtn = QPushButton("Next")
        self.nextBtn.clicked.connect(lambda: self.update_slice(self.current_slice + 1))
        
        self.buttonsLayout.addWidget(self.prevBtn)
        self.buttonsLayout.addWidget(self.playBtn)
        self.buttonsLayout.addWidget(self.nextBtn)
        
        self.layout.addWidget(self.vtkWidget)
        self.layout.addWidget(self.slider)
        self.layout.addLayout(self.buttonsLayout)

    def update_slice(self, slice_index):
        if slice_index < self.min_slice:
            slice_index = self.min_slice
        elif slice_index > self.max_slice:
            slice_index = self.max_slice
        self.current_slice = slice_index
        
        dicom_data = pydicom.dcmread(self.dicom_files[slice_index])
        pixel_array = dicom_data.pixel_array
        
        print("forma del array de pixeles:", pixel_array.shape)  

        vtk_data_array = numpy_support.numpy_to_vtk(pixel_array.ravel(), deep=True, array_type=vtk.VTK_FLOAT)
        vtk_image = vtk.vtkImageData()
        
        if pixel_array.ndim == 2:  
            vtk_image.SetDimensions(pixel_array.shape[1], pixel_array.shape[0], 1)  # (ancho, alto, profundidad=1)
        elif pixel_array.ndim == 3: 
            vtk_image.SetDimensions(pixel_array.shape[2], pixel_array.shape[1], pixel_array.shape[0])  # (ancho, alto, profundidad)
        else:
            raise ValueError("Forma de array sin soporte: {}".format(pixel_array.shape))
        
        vtk_image.GetPointData().SetScalars(vtk_data_array)
        
        self.viewer.SetInputData(vtk_image)
        self.viewer.Render()
    
    # funcion de play y pausa  
    def play_pause_btn(self):
        pass
