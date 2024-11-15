# PyQt5
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog
from mat_3d import *
# VTK
from QtOrthoViewer import *
from QtSegmentationViewer import QtSegmentationViewer
from VtkBase import VtkBase
from ViewersConnection import ViewersConnection

# Main Window
class MainWindow(QtWidgets.QMainWindow):
    
    # Constructor
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MPR Viewer")
        self.setWindowIcon(QtGui.QIcon("./app/assets/icon.ico"))
        
        # Create a central widget and set the layout
        central_widget = QtWidgets.QWidget()
        central_layout = QtWidgets.QHBoxLayout()
        
        # Create the viewers
        self.vtkBaseClass = VtkBase()
        self.QtSagittalOrthoViewer = QtOrthoViewer(self.vtkBaseClass, SLICE_ORIENTATION_YZ, "Sagital")
        self.QtCoronalOrthoViewer = QtOrthoViewer(self.vtkBaseClass, SLICE_ORIENTATION_XZ, "Coronal")
        self.QtAxialOrthoViewer = QtOrthoViewer(self.vtkBaseClass, SLICE_ORIENTATION_XY, "Axial")
        self.QtSegmentationViewer = QtSegmentationViewer(self.vtkBaseClass, label="3D")
        
        self.ViewersConnection = ViewersConnection(self.vtkBaseClass)
        self.ViewersConnection.add_orthogonal_viewer(self.QtSagittalOrthoViewer.get_viewer())
        self.ViewersConnection.add_orthogonal_viewer(self.QtCoronalOrthoViewer.get_viewer())
        self.ViewersConnection.add_orthogonal_viewer(self.QtAxialOrthoViewer.get_viewer())
        self.ViewersConnection.add_segmentation_viewer(self.QtSegmentationViewer.get_viewer())

        # Set up the main layout
        main_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        
        left_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        left_splitter.addWidget(self.QtSagittalOrthoViewer)
        left_splitter.addWidget(self.QtAxialOrthoViewer)
        
        right_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        right_splitter.addWidget(self.QtCoronalOrthoViewer)
        right_splitter.addWidget(self.QtSegmentationViewer)
        

        main_splitter.addWidget(left_splitter)
        main_splitter.addWidget(right_splitter)

        # Set the central widget
        central_layout.addWidget(main_splitter)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)
                        
        # Add menu bar
        self.create_menu()

        # Connect signals and slots
        self.connect()
    
    # Connect signals and slots         
    def connect(self):
        pass
    
    # Create the menu bar
    def create_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")

        open_action = QtWidgets.QAction("Open Image", self)
        open_action.setShortcut("Ctrl+o")

        open_action.triggered.connect(self.open_data)

        file_menu.addAction(open_action)

    # Open data
    def open_data(self):
        file_dialog = QFileDialog()
        file_paths = file_dialog.getExistingDirectory(self, "Select Folder")
        file_paths_2 = file_dialog.getExistingDirectory(self, "Select Folder 2")

        registro(file_paths, file_paths_2)
        myFile = './Data/raw/patient.mhd'
        try:
            self.load_data(myFile)
            self.render_data()
        except Exception as e:
            print(e)
            QtWidgets.QMessageBox.critical(self, "Error", "Unable to open the image file.")                    

    # Load the data
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

    # Close the application
    def closeEvent(self, QCloseEvent):
        super().closeEvent(QCloseEvent)
        self.QtAxialOrthoViewer.close()
        self.QtCoronalOrthoViewer.close()
        self.QtSagittalOrthoViewer.close()
        self.QtSegmentationViewer.close()
    
    # Exit the application  
    def exit(self):
        self.close()