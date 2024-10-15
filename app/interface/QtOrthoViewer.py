from app.interface.OrthoViewer import *
from app.interface.Worker import *
from app.interface.QtViewer import *
from app.interface.Herramientas import *


class QtOrthoViewer(QtViewer):
    # Constructor
    def __init__(self, vtkBaseClass, orientation, label: str = "Orthogonal Viewer", data: dict = None, patient: int = 0):
        super(QtOrthoViewer, self).__init__()

        # Properties
        self.orientation = orientation
        self.vtkBaseClass = vtkBaseClass
        self.status = False
        self.label = label
        self.patient = patient
        self.canvas = None  # Inicializar el Canvas como None
        self.shape_canvas = None # Inicializar
        self.distance_measurement = None  # Inicializar DistanceMeasurement como None

        # Aceptar un diccionario opcional
        self.data = data if data is not None else {}

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

        # Manejo de info_paciente
        if len(self.data) == 0:
            self.info_paciente = "No hay datos de paciente disponibles."
        else:
            # Buscar el paciente por ID
            paciente = None
            for p in self.data.values():
                if p.get('id') == self.patient:
                    paciente = p
                    break
            if paciente is None:
                self.info_paciente = "Paciente no encontrado."
            else:
                self.info_paciente = f"{paciente['apellido']}\n{paciente['nombre']}\n{paciente['documento']}\n{paciente['fecha_estudio']}"

        # Actualizar la información del paciente en el label existente
        if hasattr(self, 'info_label'):
            self.info_label.setText(self.info_paciente)
        else:
            self.info_label = QLabel(self.info_paciente, self)
            self.info_label.setStyleSheet("font-size: 12px; color: white;")
            self.layout().addWidget(self.info_label)

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
            
    # Método para inicializar Canvas
    def set_canvas(self):
        if self.canvas is None:
            # Crear e insertar el Canvas sobre el viewer
            self.canvas = Canvas(self)
            self.canvas.setFixedSize(self.viewer.size())
            self.canvas.show()

        else:
            # Si ya existe, ocultar el Canvas
            self.canvas.close()
            self.canvas = None

    # Método para inicializar DistanceMeasurement
    def set_distance_measurement(self, mhd_file):
        if self.distance_measurement is None:
            # Crear e insertar DistanceMeasurement
            self.distance_measurement = DistanceMeasurement(mhd_file, self)
            self.distance_measurement.setFixedSize(self.viewer.size())
            self.distance_measurement.show()
        else:
            # Si ya existe, ocultar DistanceMeasurement
            self.distance_measurement.close()
            self.distance_measurement = None
            
    # Método para borrar el contenido del Canvas
    def clear_canvas_drawing(self):
        if self.canvas:
            self.canvas.clear_canvas()
            print("Hola")
        if self.shape_canvas:
            self.shape_canvas.clear_canvas()
            print("Hola")
            
    def set_shape_canvas(self, shape):
        if self.shape_canvas is None:
            # Crear e insertar el Canvas sobre el viewer
            self.shape_canvas = ShapeCanvas(self)
            self.shape_canvas.setFixedSize(self.viewer.size())
            self.shape_canvas.set_shape(shape)
            self.shape_canvas.show()

        else:
            # Si ya existe, ocultar el Canvas
            self.shape_canvas.close()
            self.shape_canvas = None
