from app.interface.OrthoViewer import *
from app.interface.Worker import *
from app.interface.QtViewer import *
from model.Herramientas import *
import model.config as config
class QtOrthoViewer(QtViewer):
    # Constructor
    def __init__(self, vtkBaseClass, orientation, label: str = "Orthogonal Viewer"):
        super(QtOrthoViewer, self).__init__()

        # Properties
        self.orientation = orientation
        self.vtkBaseClass = vtkBaseClass
        self.status = False
        self.label = label
        self.canvas = None  # Inicializar el Canvas como None
        self.shape_canvas = None # Inicializar
        self.distance_measurement = None  # Inicializar DistanceMeasurement como None
        self.text_canvas = None  # Inicializar DistanceMeasurement como None
        self.angle_canvas = None # Inicializar AngleMeasurement como None
        self.image_label = None

        # Render Viewer
        self.viewer = OrthoViewer(self.vtkBaseClass, self.orientation, self.label)

        # Initialize the UI        
        self._init_UI()

        # Thread
        self.thread = QThread()
        self.worker = Worker(self.slider)

        # Connect signals and slots
        self.connect()

    # Initialize the UI
    def _init_UI(self):
        super()._init_UI()

        # PyQt Stuff
        ## Slider
        color_light = "#E2BBE9"
        color_dark = "#5A639C"
        self.slider = QSlider(Qt.Vertical)
        self.slider.setSingleStep(1)
        self.slider.setValue(0)
        self.slider.setEnabled(False)
        self.viewer.commandSliceSelect.sliders[self.orientation] = self.slider

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

        self.buttonsLayout = QHBoxLayout()

        self.prevBtn = QPushButton()
        self.prevBtn.setIcon(QIcon("./app/assets/decrease.svg"))
        self.prevBtn.setStyleSheet(
            f"font-size:15px; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px; background: {color_light}")
        self.prevBtn.setDisabled(True)

        self.playBtn = QPushButton()
        self.playBtn.setIcon(QIcon("./app/assets/play.ico"))
        self.playBtn.setStyleSheet(
            f"font-size:15px; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px; background: {color_dark}")
        self.playBtn.setDisabled(True)

        self.nextBtn = QPushButton()
        self.nextBtn.setIcon(QIcon("./app/assets/increase.svg"))
        self.nextBtn.setStyleSheet(
            f"font-size:15px; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px; background: {color_light}")
        self.nextBtn.setDisabled(True)

        self.buttonsLayout.setSpacing(10)

        self.buttonsLayout.addSpacerItem(QSpacerItem(40, 10))  # bajado a 40
        self.buttonsLayout.addWidget(self.prevBtn, 4)
        self.buttonsLayout.addWidget(self.playBtn, 5)
        self.buttonsLayout.addWidget(self.nextBtn, 4)
        self.buttonsLayout.addSpacerItem(QSpacerItem(40, 10))  # bajado a 40

        # Set up the layouts
        self.topLayout.addWidget(self.slider)
        self.mainLayout.addLayout(self.buttonsLayout)

    # Connect signals and slots        
    def connect(self):
        # Connect slider signals to slice update slots
        self.slider.valueChanged.connect(self.update_slice)

        # Connect buttons to slots
        self.prevBtn.clicked.connect(lambda: self.next_prev_btn(self.slider.value() - 10))
        self.playBtn.clicked.connect(self.play_pause_btn)
        self.nextBtn.clicked.connect(lambda: self.next_prev_btn(self.slider.value() + 10))

    # Update slice
    def update_slice(self, slice_index):
        self.viewer.set_slice(slice_index)

       # Connect on data
    def connect_on_data(self, path):
        super().connect_on_data(path)
        self.show_patient_metadata()


        # Settings of the button
        self.prevBtn.setEnabled(True)
        self.playBtn.setEnabled(True)
        self.nextBtn.setEnabled(True)

        # Settings of the slider
        self.slider.setEnabled(True)
        self.slider.setMinimum(self.viewer.min_slice)
        self.slider.setMaximum(self.viewer.max_slice)
        self.slider.setValue((self.slider.maximum() + self.slider.minimum()) // 2)



    # Next/Previous button function
    def next_prev_btn(self, slice_index):
        if slice_index < self.slider.minimum():
            slice_index = self.slider.minimum()
        elif slice_index > self.slider.maximum():
            slice_index = self.slider.maximum()

        self.slider.setValue(slice_index)
        self.viewer.set_slice(slice_index)

    # Play slices            
    def play_slices(self):
        self.thread = QThread()
        self.worker = Worker(self.slider)
        self.status = True

        # Play Button icon
        self.playBtn.setIcon(QIcon("./app/assets/pause.ico"))

        # Final resets
        # Move worker to the thread
        self.worker.moveToThread(self.thread)

        # Connect signals and slots
        self.thread.started.connect(self.worker.play)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.update_slice)

        # Start the thread
        self.thread.start()
        self.slider.setHidden(True)
        self.thread.finished.connect(
            lambda: self.slider.setHidden(False)
        )
        self.thread.finished.connect(
            self.pause_slices
        )

    # Pause slices
    def pause_slices(self):
        self.playBtn.setIcon(QIcon("./app/assets/play.ico"))
        self.worker.pause()
        self.status = False

    # Play/Pause button function    
    def play_pause_btn(self):
        if self.status is False:
            self.play_slices()
        else:
            self.pause_slices()

     # Método para mostrar la metadata del paciente
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

    def capture_vtk_image(self):
        """Captura el renderizado actual de VTK como QPixmap."""
        # Configurar el filtro para capturar la ventana de VTK
        window_to_image_filter = vtk.vtkWindowToImageFilter()
        window_to_image_filter.SetInput(self.viewer.GetRenderWindow())
        window_to_image_filter.Update()

        # Guardar la imagen en PNG usando vtkPNGWriter
        png_writer = vtk.vtkPNGWriter()
        png_writer.SetFileName("./temp/image1.png")
        png_writer.SetInputConnection(window_to_image_filter.GetOutputPort())
        png_writer.Write()

        # Cargar la imagen guardada como QPixmap
        pixmap = QPixmap("./temp/image1.png")

        # Crear un QLabel para mostrar la imagen
        self.image_label = QLabel(self)
        self.image_label.setPixmap(pixmap.scaled(self.width(), self.height(), aspectRatioMode=Qt.KeepAspectRatio))
        self.image_label.setGeometry(0, 0, self.width(), self.height())
        self.image_label.show()

    # Método para inicializar Canvas
    def set_canvas(self):
        if self.canvas is None:
            # Crear e insertar el Canvas sobre el viewer
            self.capture_vtk_image()
            self.canvas = Canvas(self)
            self.canvas.show()

        else:
            self.clear_tools()

    # Método para inicializar DistanceMeasurement
    def set_distance_measurement(self, mhd_file):
        if self.distance_measurement is None:
            # Crear e insertar DistanceMeasurement
            self.capture_vtk_image()
            self.distance_measurement = DistanceMeasurement(mhd_file, self)
            self.distance_measurement.show()
        else:
            self.clear_tools()
            
    def set_shape_canvas(self, shape):
        if self.shape_canvas is None:
            # Crear e insertar el Canvas sobre el viewer
            self.capture_vtk_image()
            self.shape_canvas = ShapeCanvas(self)
            self.shape_canvas.set_shape(shape)
            self.shape_canvas.show()

        else:
            self.clear_tools()

    def set_text_canvas(self):
        if self.text_canvas is None:
            self.capture_vtk_image()
            self.text_canvas = TextCanvas(self)
            self.text_canvas.show()
        else:
            self.clear_tools()

    def set_angle_canvas(self):
        if self.angle_canvas is None:
            self.capture_vtk_image()
            self.angle_canvas = AngleMeasurement(self)
            self.angle_canvas.show()
        else:
            self.clear_tools()

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

    def clear_tools(self):
        if self.canvas is not None:
            self.canvas.close()
            self.canvas = None
            self.image_label.close()
            self.image_label = None

        if self.distance_measurement is not None:
            self.distance_measurement.close()
            self.distance_measurement = None
            self.image_label.close()
            self.image_label = None

        if self.shape_canvas is not None:
            self.shape_canvas.close()
            self.shape_canvas = None
            self.image_label.close()
            self.image_label = None

        if self.text_canvas is not None:
            self.text_canvas.close()
            self.text_canvas = None
            self.image_label.close()
            self.image_label = None

        if self.angle_canvas is not None:
            self.angle_canvas.close()
            self.angle_canvas = None
            self.image_label.close()
            self.image_label = None

