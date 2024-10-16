from actions import ViewerActions
from app.interface.QtOrthoViewer import *
from app.interface.QtSegmentationViewer import *
from app.interface.VtkBase import *
from app.interface.ViewersConnection import *
#Metodo para crear el registro de las imagenes 
from app.interface.mat_3d import registro
from Dicom_vis.DicomViewer import *
import config
from PyQt5.QtGui import QPen
from PyQt5.QtGui import QPainter, QPen, QMouseEvent
from PyQt5.QtCore import Qt, QPoint
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
        def setupUi(self, MainWindow):

                MainWindow.setObjectName("MainWindow")
                MainWindow.resize(869, 600)
                MainWindow.setMinimumSize(QtCore.QSize(800, 600))
                MainWindow.setMaximumSize(QtCore.QSize(1920, 1080))
                MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
                #Definición de Orthoviewers a utilizar
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
                # Prueba para el visualizador de dicom
                self.dcm_viewer = DicomViewer('Axial')
                viewers = (self.QtSagittalOrthoViewer, self.QtAxialOrthoViewer, self.QtCoronalOrthoViewer, self.QtSegmentationViewer)
                self.centralwidget = QtWidgets.QWidget(MainWindow)
                self.centralwidget.setObjectName("centralwidget")
                self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
                self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
                self.horizontalLayout.setSpacing(0)
                self.horizontalLayout.setObjectName("horizontalLayout")
                self.frame = QtWidgets.QFrame(self.centralwidget)
                self.frame.setMinimumSize(QtCore.QSize(70, 0))
                self.frame.setMaximumSize(QtCore.QSize(70, 16777215))
                self.frame.setStyleSheet("background-color:rgb(90, 99, 156)")
                self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
                self.frame.setObjectName("frame")
                self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
                self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
                self.verticalLayout_2.setSpacing(2)
                self.verticalLayout_2.setObjectName("verticalLayout_2")
                self.frame_9 = QtWidgets.QFrame(self.frame)
                self.frame_9.setFrameShape(QtWidgets.QFrame.NoFrame)
                self.frame_9.setObjectName("frame_9")
                self.verticalLayout_2.addWidget(self.frame_9)
                self.frame_10 = QtWidgets.QFrame(self.frame)
                self.frame_10.setStyleSheet("QPushButton{\n"
                "\n"
                "border-radius: 25px;\n"
                "}\n"
                "\n"
                "QPushButton:checked{\n"
                "background-color:#E2BBE9;\n"
                "\n"
                "}\n"
                "\n"
                "")
                self.frame_10.setFrameShape(QtWidgets.QFrame.NoFrame)
                self.frame_10.setObjectName("frame_10")
                self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_10)
                self.verticalLayout_3.setObjectName("verticalLayout_3")
                self.mainButton_DB = QtWidgets.QPushButton(self.frame_10)
                self.mainButton_DB.setMinimumSize(QtCore.QSize(50, 50))
                self.mainButton_DB.setMaximumSize(QtCore.QSize(50, 50))
                self.mainButton_DB.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.mainButton_DB.setStyleSheet("border:0px;")
                self.mainButton_DB.setText("")
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(".\\Assets/database_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.mainButton_DB.setIcon(icon)
                self.mainButton_DB.setIconSize(QtCore.QSize(50, 50))
                self.mainButton_DB.setCheckable(True)
                self.mainButton_DB.setChecked(True)
                self.mainButton_DB.setAutoExclusive(True)
                self.mainButton_DB.setObjectName("mainButton_DB")
                self.verticalLayout_3.addWidget(self.mainButton_DB)
                self.mainButton_visualizacion = QtWidgets.QPushButton(self.frame_10)
                self.mainButton_visualizacion.setMinimumSize(QtCore.QSize(50, 50))
                self.mainButton_visualizacion.setMaximumSize(QtCore.QSize(50, 50))
                self.mainButton_visualizacion.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.mainButton_visualizacion.setText("")
                icon1 = QtGui.QIcon()
                icon1.addPixmap(QtGui.QPixmap(":/icons/Assets/display_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.mainButton_visualizacion.setIcon(icon1)
                self.mainButton_visualizacion.setIconSize(QtCore.QSize(4000, 50))
                self.mainButton_visualizacion.setCheckable(True)
                self.mainButton_visualizacion.setChecked(False)
                self.mainButton_visualizacion.setAutoExclusive(True)
                self.mainButton_visualizacion.setObjectName("mainButton_visualizacion")
                self.verticalLayout_3.addWidget(self.mainButton_visualizacion)
                self.mainButton_anadirArchivo = QtWidgets.QPushButton(self.frame_10)
                self.mainButton_anadirArchivo.setMinimumSize(QtCore.QSize(50, 50))
                self.mainButton_anadirArchivo.setMaximumSize(QtCore.QSize(50, 50))
                self.mainButton_anadirArchivo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.mainButton_anadirArchivo.setStyleSheet("border:0px;")
                self.mainButton_anadirArchivo.setText("")
                icon2 = QtGui.QIcon()
                icon2.addPixmap(QtGui.QPixmap(".\\Assets/addDicom_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.mainButton_anadirArchivo.setIcon(icon2)
                self.mainButton_anadirArchivo.setIconSize(QtCore.QSize(50, 50))
                self.mainButton_anadirArchivo.setCheckable(True)
                self.mainButton_anadirArchivo.setAutoExclusive(True)
                self.mainButton_anadirArchivo.setObjectName("mainButton_anadirArchivo")
                self.verticalLayout_3.addWidget(self.mainButton_anadirArchivo)
                self.verticalLayout_2.addWidget(self.frame_10)
                self.frame_11 = QtWidgets.QFrame(self.frame)
                self.frame_11.setFrameShape(QtWidgets.QFrame.NoFrame)
                self.frame_11.setObjectName("frame_11")
                self.verticalLayout_2.addWidget(self.frame_11)
                self.horizontalLayout.addWidget(self.frame)
                self.stackedWidgetPrincipal = QtWidgets.QStackedWidget(self.centralwidget)
                self.stackedWidgetPrincipal.setObjectName("stackedWidgetPrincipal")
                self.pantallaVisualizacion = QtWidgets.QWidget()
                self.pantallaVisualizacion.setStyleSheet("\n"
                "background-color: rgb(0, 0, 0);")
                self.pantallaVisualizacion.setObjectName("pantallaVisualizacion")
                self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.pantallaVisualizacion)
                self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
                self.horizontalLayout_5.setObjectName("horizontalLayout_5")
                self.frame_2 = QtWidgets.QFrame(self.pantallaVisualizacion)
                self.frame_2.setMaximumSize(QtCore.QSize(270, 16777215))
                self.frame_2.setStyleSheet("background-color: rgb(255, 255, 255)")
                self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
                self.frame_2.setObjectName("frame_2")
                self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_2)
                self.verticalLayout.setContentsMargins(0, 0, 0, 0)
                self.verticalLayout.setObjectName("verticalLayout")
                self.frame_17 = QtWidgets.QFrame(self.frame_2)
                self.frame_17.setMinimumSize(QtCore.QSize(272, 70))
                self.frame_17.setMaximumSize(QtCore.QSize(250, 70))
                self.frame_17.setStyleSheet("background-color: #5A639C;\n"
                "border-radius: 30px;\n"
                "\n"
                "\n"
                "")
                self.frame_17.setFrameShape(QtWidgets.QFrame.NoFrame)
                self.frame_17.setObjectName("frame_17")
                self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_17)
                self.horizontalLayout_6.setObjectName("horizontalLayout_6")
                self.subMenu_patient = QtWidgets.QPushButton(self.frame_17)
                self.subMenu_patient.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.subMenu_patient.setStyleSheet("QPushButton:checked{\n"
                "background-color:#E2BBE9;\n"
                "border-radius: 20px\n"
                "}\n"
                "")
                self.subMenu_patient.setText("")
                icon3 = QtGui.QIcon()
                icon3.addPixmap(QtGui.QPixmap(".\\Assets/subMenu_patient.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.subMenu_patient.setIcon(icon3)
                self.subMenu_patient.setIconSize(QtCore.QSize(50, 50))
                self.subMenu_patient.setCheckable(True)
                self.subMenu_patient.setChecked(True)
                self.subMenu_patient.setAutoExclusive(True)
                self.subMenu_patient.setAutoRepeatInterval(103)
                self.subMenu_patient.setObjectName("subMenu_patient")
                self.horizontalLayout_6.addWidget(self.subMenu_patient)
                self.subMenu_tools = QtWidgets.QPushButton(self.frame_17)
                self.subMenu_tools.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.subMenu_tools.setStyleSheet("QPushButton:checked{\n"
                "background-color:#E2BBE9;\n"
                "border-radius: 20px\n"
                "}\n"
                "")
                self.subMenu_tools.setText("")
                icon4 = QtGui.QIcon()
                icon4.addPixmap(QtGui.QPixmap(".\\Assets/subMenu_tools.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.subMenu_tools.setIcon(icon4)
                self.subMenu_tools.setIconSize(QtCore.QSize(50, 50))
                self.subMenu_tools.setCheckable(True)
                self.subMenu_tools.setAutoExclusive(True)
                self.subMenu_tools.setObjectName("subMenu_tools")
                self.horizontalLayout_6.addWidget(self.subMenu_tools)
                self.verticalLayout.addWidget(self.frame_17)
                spacerItem = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
                self.verticalLayout.addItem(spacerItem)
                self.stackedWidget_submenuVisualizacion = QtWidgets.QStackedWidget(self.frame_2)
                self.stackedWidget_submenuVisualizacion.setObjectName("stackedWidget_submenuVisualizacion")
                self.submenuPatient = QtWidgets.QWidget()
                self.submenuPatient.setEnabled(True)
                self.submenuPatient.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.submenuPatient.setStyleSheet("")
                self.submenuPatient.setObjectName("submenuPatient")
                self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.submenuPatient)
                self.verticalLayout_8.setObjectName("verticalLayout_8")
                self.frame_15 = QtWidgets.QFrame(self.submenuPatient)
                self.frame_15.setMinimumSize(QtCore.QSize(200, 250))
                self.frame_15.setMaximumSize(QtCore.QSize(16777215, 240))
                self.frame_15.setStyleSheet("background-color: #FFFFFF;\n"
                "\n"
                "")
                self.frame_15.setFrameShape(QtWidgets.QFrame.NoFrame)
                self.frame_15.setObjectName("frame_15")
                self.frame_18 = QtWidgets.QFrame(self.frame_15)
                self.frame_18.setGeometry(QtCore.QRect(0, 20, 250, 200))
                self.frame_18.setMinimumSize(QtCore.QSize(250, 0))
                self.frame_18.setMaximumSize(QtCore.QSize(250, 200))
                self.frame_18.setStyleSheet("background-color: #E8C9ED;\n"
                "border-radius: 15px;")
                self.frame_18.setFrameShape(QtWidgets.QFrame.NoFrame)
                self.frame_18.setObjectName("frame_18")
                self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.frame_18)
                self.verticalLayout_9.setContentsMargins(0, 18, 0, -1)
                self.verticalLayout_9.setObjectName("verticalLayout_9")
                self.patientInfo_table = QtWidgets.QTableWidget(self.frame_18)
                font = QtGui.QFont()
                font.setFamily("Roboto")
                self.patientInfo_table.setFont(font)
                self.patientInfo_table.setStyleSheet("\n"
                "QTableWidget::item {\n"
                "    text-align: center;\n"
                "\n"
                "}")
                self.patientInfo_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                self.patientInfo_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                self.patientInfo_table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
                self.patientInfo_table.setCornerButtonEnabled(False)
                self.patientInfo_table.setObjectName("patientInfo_table")
                self.patientInfo_table.setColumnCount(2)
                self.patientInfo_table.setRowCount(0)
                item = QtWidgets.QTableWidgetItem()
                self.patientInfo_table.setHorizontalHeaderItem(0, item)
                item = QtWidgets.QTableWidgetItem()
                self.patientInfo_table.setHorizontalHeaderItem(1, item)
                self.patientInfo_table.horizontalHeader().setVisible(False)
                self.patientInfo_table.horizontalHeader().setStretchLastSection(True)
                self.patientInfo_table.verticalHeader().setVisible(False)
                self.patientInfo_table.verticalHeader().setStretchLastSection(True)
                self.verticalLayout_9.addWidget(self.patientInfo_table)
                self.label_9 = QtWidgets.QLabel(self.frame_15)
                self.label_9.setGeometry(QtCore.QRect(40, 0, 171, 31))
                self.label_9.setStyleSheet("font: 87 16pt \"Roboto\" \"bold\";\n"
                "background-color: rgb(119, 118, 179);\n"
                "color:#FFFFFF;\n"
                "border-radius: 15px;")
                self.label_9.setTextFormat(QtCore.Qt.PlainText)
                self.label_9.setAlignment(QtCore.Qt.AlignCenter)
                self.label_9.setObjectName("label_9")
                self.verticalLayout_8.addWidget(self.frame_15)
                self.frame_19 = QtWidgets.QFrame(self.submenuPatient)
                self.frame_19.setMinimumSize(QtCore.QSize(200, 250))
                self.frame_19.setMaximumSize(QtCore.QSize(16777215, 240))
                self.frame_19.setStyleSheet("background-color: #FFFFFF;\n"
                "\n"
                "")
                self.frame_19.setFrameShape(QtWidgets.QFrame.NoFrame)
                self.frame_19.setObjectName("frame_19")
                self.frame_20 = QtWidgets.QFrame(self.frame_19)
                self.frame_20.setGeometry(QtCore.QRect(0, 20, 250, 300))
                self.frame_20.setMinimumSize(QtCore.QSize(250, 0))
                self.frame_20.setMaximumSize(QtCore.QSize(250, 200))
                self.frame_20.setStyleSheet("background-color: #E8C9ED;\n"
                "border-radius: 15px;")
                self.frame_20.setFrameShape(QtWidgets.QFrame.NoFrame)
                self.frame_20.setObjectName("frame_20")
                self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.frame_20)
                self.verticalLayout_10.setContentsMargins(0, -1, 0, -1)
                self.verticalLayout_10.setObjectName("verticalLayout_10")
                self.studyInfo_table = QtWidgets.QTableWidget(self.frame_20)
                font = QtGui.QFont()
                font.setFamily("Roboto")
                self.studyInfo_table.setFont(font)
                self.studyInfo_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                self.studyInfo_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                self.studyInfo_table.setObjectName("studyInfo_table")
                self.studyInfo_table.setColumnCount(2)
                self.studyInfo_table.setRowCount(0)
                item = QtWidgets.QTableWidgetItem()
                self.studyInfo_table.setHorizontalHeaderItem(0, item)
                item = QtWidgets.QTableWidgetItem()
                self.studyInfo_table.setHorizontalHeaderItem(1, item)
                self.studyInfo_table.horizontalHeader().setVisible(False)
                self.studyInfo_table.horizontalHeader().setStretchLastSection(True)
                self.studyInfo_table.verticalHeader().setVisible(False)
                self.studyInfo_table.verticalHeader().setStretchLastSection(True)
                self.verticalLayout_10.addWidget(self.studyInfo_table)
                self.label_11 = QtWidgets.QLabel(self.frame_19)
                self.label_11.setGeometry(QtCore.QRect(40, 0, 171, 31))
                self.label_11.setStyleSheet("font: 87 16pt \"Roboto\" \"bold\";\n"
                "background-color: rgb(119, 118, 179);\n"
                "color:#FFFFFF;\n"
                "border-radius: 15px;")
                self.label_11.setTextFormat(QtCore.Qt.PlainText)
                self.label_11.setAlignment(QtCore.Qt.AlignCenter)
                self.label_11.setObjectName("label_11")
                self.verticalLayout_8.addWidget(self.frame_19)
                spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                self.verticalLayout_8.addItem(spacerItem1)
                self.stackedWidget_submenuVisualizacion.addWidget(self.submenuPatient)
                self.submenuTools = QtWidgets.QWidget()
                self.submenuTools.setObjectName("submenuTools")
                self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.submenuTools)
                self.verticalLayout_4.setObjectName("verticalLayout_4")
                self.frame_12 = QtWidgets.QFrame(self.submenuTools)
                self.frame_12.setMinimumSize(QtCore.QSize(200, 190))
                self.frame_12.setMaximumSize(QtCore.QSize(16777215, 190))
                self.frame_12.setStyleSheet("background-color: #FFFFFF;\n"
                "\n"
                "")
                self.frame_12.setFrameShape(QtWidgets.QFrame.NoFrame)
                self.frame_12.setObjectName("frame_12")
                self.frame_13 = QtWidgets.QFrame(self.frame_12)
                self.frame_13.setGeometry(QtCore.QRect(0, 20, 250, 161))
                self.frame_13.setMinimumSize(QtCore.QSize(250, 0))
                self.frame_13.setMaximumSize(QtCore.QSize(250, 200))
                self.frame_13.setStyleSheet("background-color: #E8C9ED;\n"
                "border-radius: 15px;")
                self.frame_13.setFrameShape(QtWidgets.QFrame.NoFrame)
                self.frame_13.setObjectName("frame_13")
                self.gridLayoutWidget = QtWidgets.QWidget(self.frame_13)
                self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 10, 251, 154))
                self.gridLayoutWidget.setObjectName("gridLayoutWidget")
                self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
                self.gridLayout.setContentsMargins(5, 5, 5, 5)
                self.gridLayout.setHorizontalSpacing(0)
                self.gridLayout.setObjectName("gridLayout")
                self.toolButton_filtros = QtWidgets.QPushButton(self.gridLayoutWidget)
                self.toolButton_filtros.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                icon5 = QtGui.QIcon()
                icon5.addPixmap(QtGui.QPixmap(".\\Assets/colorfilter.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.toolButton_filtros.setIcon(icon5)
                self.toolButton_filtros.setIconSize(QtCore.QSize(40, 40))
                self.toolButton_filtros.setObjectName("toolButton_filtros")
                self.toolButton_filtros.setToolTip("Aplicar filtros sobre los estudios")
                self.toolButton_filtros.setCheckable(True)
                self.gridLayout.addWidget(self.toolButton_filtros, 0, 2, 1, 1)
                self.toolButton_regla = QtWidgets.QPushButton(self.gridLayoutWidget)
                self.toolButton_regla.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                icon6 = QtGui.QIcon()
                icon6.addPixmap(QtGui.QPixmap(":/icons/Assets/ruler.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.toolButton_regla.setIcon(icon6)
                self.toolButton_regla.setIconSize(QtCore.QSize(40, 40))
                self.toolButton_regla.setObjectName("toolButton_regla")
                self.toolButton_regla.clicked.connect(self.activate_distance_measurement)
                self.toolButton_regla.setToolTip("Realizar mediciones sobre los estudios")
                self.toolButton_regla.setCheckable(True)
                self.measurement_view = None
                self.gridLayout.addWidget(self.toolButton_regla, 0, 0, 1, 1)
                self.toolButton_areaCircular = QtWidgets.QPushButton(self.gridLayoutWidget)
                self.toolButton_areaCircular.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                icon7 = QtGui.QIcon()
                icon7.addPixmap(QtGui.QPixmap(".\\Assets/Ellipse.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.toolButton_areaCircular.setIcon(icon7)
                self.toolButton_areaCircular.setIconSize(QtCore.QSize(45, 45))
                self.toolButton_areaCircular.setObjectName("toolButton_areaCircular")
                self.toolButton_areaCircular.setToolTip("Encontrar el área circular dentro del estudio")
                self.toolButton_areaCircular.clicked.connect(lambda: self.set_shape_canvas("circle"))
                self.toolButton_areaCircular.setCheckable(True)
                self.gridLayout.addWidget(self.toolButton_areaCircular, 1, 0, 1, 1)
                self.toolButton_flechas = QtWidgets.QPushButton(self.gridLayoutWidget)
                self.toolButton_flechas.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                icon8 = QtGui.QIcon()
                icon8.addPixmap(QtGui.QPixmap(".\\Assets/Arrow 1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.toolButton_flechas.setIcon(icon8)
                self.toolButton_flechas.setIconSize(QtCore.QSize(35, 35))
                self.toolButton_flechas.setObjectName("toolButton_flechas")
                self.toolButton_flechas.setToolTip("Dibujar flechas")
                self.toolButton_flechas.clicked.connect(lambda: self.set_shape_canvas("arrow"))
                self.toolButton_flechas.setCheckable(True)
                self.gridLayout.addWidget(self.toolButton_flechas, 1, 3, 1, 1)
                self.toolButton_dibujoLibre = QtWidgets.QPushButton(self.gridLayoutWidget)
                self.toolButton_dibujoLibre.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                icon9 = QtGui.QIcon()
                icon9.addPixmap(QtGui.QPixmap(".\\Assets/freeDraw.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.toolButton_dibujoLibre.setIcon(icon9)
                self.toolButton_dibujoLibre.setIconSize(QtCore.QSize(40, 40))
                self.toolButton_dibujoLibre.setObjectName("toolButton_dibujoLibre")
                self.toolButton_dibujoLibre.setToolTip("Iniciar dibujo libre sobre la imagen")
                self.toolButton_dibujoLibre.clicked.connect(self.set_canvas)
                self.toolButton_dibujoLibre.setCheckable(True)
                self.canvas = None
                self.gridLayout.addWidget(self.toolButton_dibujoLibre, 0, 1, 1, 1)
                self.toolButton_angulos = QtWidgets.QPushButton(self.gridLayoutWidget)
                self.toolButton_angulos.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                icon10 = QtGui.QIcon()
                icon10.addPixmap(QtGui.QPixmap(".\\Assets/Angle.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.toolButton_angulos.setIcon(icon10)
                self.toolButton_angulos.setIconSize(QtCore.QSize(40, 40))
                self.toolButton_angulos.setObjectName("toolButton_angulos")
                self.toolButton_angulos.setToolTip("Encontrar ángulos dentro de los estudios")
                self.toolButton_angulos.setCheckable(True)
                self.gridLayout.addWidget(self.toolButton_angulos, 1, 2, 1, 1)
                self.toolButton_descargaImagen = QtWidgets.QPushButton(self.gridLayoutWidget)
                self.toolButton_descargaImagen.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                icon11 = QtGui.QIcon()
                icon11.addPixmap(QtGui.QPixmap(".\\Assets/gallery-import.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.toolButton_descargaImagen.setIcon(icon11)
                self.toolButton_descargaImagen.setIconSize(QtCore.QSize(45, 40))
                self.toolButton_descargaImagen.setObjectName("toolButton_descargaImagen")
                self.toolButton_descargaImagen.setToolTip("Descargar imagen con las notaciones realizadas")
                self.gridLayout.addWidget(self.toolButton_descargaImagen, 2, 1, 1, 1)
                self.toolButton_borrador = QtWidgets.QPushButton(self.gridLayoutWidget)
                self.toolButton_borrador.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                icon12 = QtGui.QIcon()
                icon12.addPixmap(QtGui.QPixmap(".\\Assets/eraser.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.toolButton_borrador.setIcon(icon12)
                self.toolButton_borrador.setIconSize(QtCore.QSize(45, 45))
                self.toolButton_borrador.setObjectName("toolButton_borrador")
                self.toolButton_borrador.setToolTip("Borrar dibujos realizados")
                self.toolButton_borrador.clicked.connect(self.clear_canvas_drawing)
                self.toolButton_borrador.setStyleSheet("""
                QPushButton:pressed {
                        background-color: #a0a0a0; /* Color de fondo al presionar */
                        border: 2px solid #808080; /* Bordes al presionar */
                }
                """)
                self.gridLayout.addWidget(self.toolButton_borrador, 2, 0, 1, 1)
                self.toolButton_areaRectangular = QtWidgets.QPushButton(self.gridLayoutWidget)
                self.toolButton_areaRectangular.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                icon13 = QtGui.QIcon()
                icon13.addPixmap(QtGui.QPixmap(".\\Assets/Rectangle 20.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.toolButton_areaRectangular.setIcon(icon13)
                self.toolButton_areaRectangular.setIconSize(QtCore.QSize(40, 40))
                self.toolButton_areaRectangular.setObjectName("toolButton_areaRectangular")
                self.toolButton_areaRectangular.setToolTip("Encontrar el área rectangular dentro de los estudios")
                self.toolButton_areaRectangular.clicked.connect(lambda: self.set_shape_canvas("square"))
                self.toolButton_areaRectangular.setCheckable(True)
                self.gridLayout.addWidget(self.toolButton_areaRectangular, 1, 1, 1, 1)
                self.toolButton_escritura = QtWidgets.QPushButton(self.gridLayoutWidget)
                self.toolButton_escritura.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                icon14 = QtGui.QIcon()
                icon14.addPixmap(QtGui.QPixmap(".\\Assets/A.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.toolButton_escritura.setIcon(icon14)
                self.toolButton_escritura.setIconSize(QtCore.QSize(35, 35))
                self.toolButton_escritura.setObjectName("toolButton_escritura")
                self.toolButton_escritura.clicked.connect(self.set_text_canvas)
                self.toolButton_escritura.setToolTip("Escribir encima de los estudios")
                self.toolButton_escritura.setCheckable(True)
                self.gridLayout.addWidget(self.toolButton_escritura, 0, 3, 1, 1)
                self.label_8 = QtWidgets.QLabel(self.frame_12)
                self.label_8.setGeometry(QtCore.QRect(40, 0, 171, 31))
                self.label_8.setStyleSheet("font: 87 16pt \"Roboto\" \"bold\";\n"
                "background-color: rgb(119, 118, 179);\n"
                "color:#FFFFFF;\n"
                "border-radius: 15px;")
                self.label_8.setTextFormat(QtCore.Qt.PlainText)
                self.label_8.setAlignment(QtCore.Qt.AlignCenter)
                self.label_8.setObjectName("label_8")
                self.verticalLayout_4.addWidget(self.frame_12)
                self.frame_14 = QtWidgets.QFrame(self.submenuTools)
                self.frame_14.setMinimumSize(QtCore.QSize(250, 100))
                self.frame_14.setMaximumSize(QtCore.QSize(16777215, 100))
                self.frame_14.setStyleSheet("background-color: #FFFFFF;\n"
                "\n"
                "")
                self.frame_14.setFrameShape(QtWidgets.QFrame.NoFrame)
                self.frame_14.setObjectName("frame_14")
                self.frame_16 = QtWidgets.QFrame(self.frame_14)
                self.frame_16.setGeometry(QtCore.QRect(0, 20, 250, 71))
                self.frame_16.setMinimumSize(QtCore.QSize(0, 0))
                self.frame_16.setMaximumSize(QtCore.QSize(250, 200))
                self.frame_16.setStyleSheet("background-color: #E8C9ED;\n"
                "border-radius: 15px;")
                self.frame_16.setFrameShape(QtWidgets.QFrame.NoFrame)
                self.frame_16.setObjectName("frame_16")
                self.gridLayoutWidget_3 = QtWidgets.QWidget(self.frame_16)
                self.gridLayoutWidget_3.setGeometry(QtCore.QRect(0, 10, 251, 61))
                self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
                self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
                self.gridLayout_3.setContentsMargins(5, 5, 5, 5)
                self.gridLayout_3.setHorizontalSpacing(0)
                self.gridLayout_3.setObjectName("gridLayout_3")
                self.functionButton_brillo = QtWidgets.QPushButton(self.gridLayoutWidget_3)
                self.functionButton_brillo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                icon15 = QtGui.QIcon()
                icon15.addPixmap(QtGui.QPixmap(".\\Assets/brightness.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.functionButton_brillo.setIcon(icon15)
                self.functionButton_brillo.setIconSize(QtCore.QSize(40, 40))
                self.functionButton_brillo.setObjectName("functionButton_brillo")
                self.functionButton_brillo.setToolTip("Cambiar el brillo de los estudios")
                self.functionButton_brillo.setCheckable(True)
                self.gridLayout_3.addWidget(self.functionButton_brillo, 0, 2, 1, 1)
                self.functionButton_rotacion = QtWidgets.QPushButton(self.gridLayoutWidget_3)
                self.functionButton_rotacion.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                icon16 = QtGui.QIcon()
                icon16.addPixmap(QtGui.QPixmap(".\\Assets/refresh-circle.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.functionButton_rotacion.setIcon(icon16)
                self.functionButton_rotacion.setIconSize(QtCore.QSize(50, 50))
                self.functionButton_rotacion.setObjectName("functionButton_rotacion")
                self.functionButton_rotacion.setToolTip("Rotar los estudios")
                self.functionButton_rotacion.setCheckable(True)
                self.gridLayout_3.addWidget(self.functionButton_rotacion, 0, 1, 1, 1)
                self.functionButton_desplazamiento = QtWidgets.QPushButton(self.gridLayoutWidget_3)
                self.functionButton_desplazamiento.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                icon17 = QtGui.QIcon()
                icon17.addPixmap(QtGui.QPixmap(".\\Assets/displacement.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.functionButton_desplazamiento.setIcon(icon17)
                self.functionButton_desplazamiento.setIconSize(QtCore.QSize(50, 50))
                self.functionButton_desplazamiento.setObjectName("functionButton_desplazamiento")
                self.functionButton_desplazamiento.setToolTip("Realizar desplazamientos")
                self.functionButton_desplazamiento.setCheckable(True)
                self.gridLayout_3.addWidget(self.functionButton_desplazamiento, 0, 0, 1, 1)
                self.label_10 = QtWidgets.QLabel(self.frame_14)
                self.label_10.setGeometry(QtCore.QRect(40, 0, 171, 31))
                self.label_10.setStyleSheet("font: 87 16pt \"Roboto\" \"bold\";\n"
                "background-color: rgb(119, 118, 179);\n"
                "color:#FFFFFF;\n"
                "border-radius: 15px;")
                self.label_10.setTextFormat(QtCore.Qt.PlainText)
                self.label_10.setAlignment(QtCore.Qt.AlignCenter)
                self.label_10.setObjectName("label_10")
                self.verticalLayout_4.addWidget(self.frame_14)
                self.frame_22 = QtWidgets.QFrame(self.submenuTools)
                self.frame_22.setMinimumSize(QtCore.QSize(0, 160))
                self.frame_22.setMaximumSize(QtCore.QSize(16777215, 225))
                self.frame_22.setStyleSheet("background-color: #FFFFFF;\n"
                "\n"
                "")
                self.frame_22.setFrameShape(QtWidgets.QFrame.NoFrame)
                self.frame_22.setObjectName("frame_22")
                self.frame_23 = QtWidgets.QFrame(self.frame_22)
                self.frame_23.setGeometry(QtCore.QRect(0, 20, 250, 131))
                self.frame_23.setMinimumSize(QtCore.QSize(250, 0))
                self.frame_23.setMaximumSize(QtCore.QSize(250, 200))
                self.frame_23.setStyleSheet("background-color: #E8C9ED;\n"
                "border-radius: 15px;")
                self.frame_23.setFrameShape(QtWidgets.QFrame.NoFrame)
                self.frame_23.setObjectName("frame_23")
                self.gridLayoutWidget_7 = QtWidgets.QWidget(self.frame_23)
                self.gridLayoutWidget_7.setGeometry(QtCore.QRect(0, 10, 251, 121))
                self.gridLayoutWidget_7.setObjectName("gridLayoutWidget_7")
                self.gridLayout_7 = QtWidgets.QGridLayout(self.gridLayoutWidget_7)
                self.gridLayout_7.setContentsMargins(5, 5, 5, 5)
                self.gridLayout_7.setHorizontalSpacing(0)
                self.gridLayout_7.setObjectName("gridLayout_7")
                self.dispositionButton_2x2 = QtWidgets.QPushButton(self.gridLayoutWidget_7)
                self.dispositionButton_2x2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                icon18 = QtGui.QIcon()
                icon18.addPixmap(QtGui.QPixmap(".\\Assets/2x2 grid.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.dispositionButton_2x2.setIcon(icon18)
                self.dispositionButton_2x2.setIconSize(QtCore.QSize(45, 45))
                self.dispositionButton_2x2.setObjectName("dispositionButton_2x2")
                self.dispositionButton_2x2.setToolTip("Mostrar disposición 2x2 (Sagital) (Axial) (Coronal) (3D)")
                self.dispositionButton_2x2.clicked.connect(self.display_four_images)
                self.dispositionButton_2x2.setCheckable(True)
                self.gridLayout_7.addWidget(self.dispositionButton_2x2, 1, 1, 1, 1)
                self.dispositionButton_1x1 = QtWidgets.QPushButton(self.gridLayoutWidget_7)
                self.dispositionButton_1x1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                icon19 = QtGui.QIcon()
                icon19.addPixmap(QtGui.QPixmap(".\\Assets/Rectangle 24.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.dispositionButton_1x1.setIcon(icon19)
                self.dispositionButton_1x1.setIconSize(QtCore.QSize(45, 45))
                self.dispositionButton_1x1.setObjectName("dispositionButton_1x1")
                self.dispositionButton_1x1.setToolTip("Mostrar disposición 1x1 (Sagital)")
                self.dispositionButton_1x1.clicked.connect(self.display_one_image)
                self.dispositionButton_1x1.setCheckable(True)
                self.gridLayout_7.addWidget(self.dispositionButton_1x1, 0, 0, 1, 1)
                self.dispositionButton_2x1 = QtWidgets.QPushButton(self.gridLayoutWidget_7)
                self.dispositionButton_2x1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                icon20 = QtGui.QIcon()
                icon20.addPixmap(QtGui.QPixmap(".\\Assets/2x1grid.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.dispositionButton_2x1.setIcon(icon20)
                self.dispositionButton_2x1.setIconSize(QtCore.QSize(35, 35))
                self.dispositionButton_2x1.setToolTip("Mostrar disposición 2x1 (Sagital) arriba (Axial) abajo")
                self.dispositionButton_2x1.clicked.connect(self.display_two_images_vertical)
                self.dispositionButton_2x1.setCheckable(True)
                self.gridLayout_7.addWidget(self.dispositionButton_2x1, 0, 3, 1, 1)
                self.dispositionButton_1x3 = QtWidgets.QPushButton(self.gridLayoutWidget_7)
                self.dispositionButton_1x3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                icon21 = QtGui.QIcon()
                icon21.addPixmap(QtGui.QPixmap(".\\Assets/1x3grid.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.dispositionButton_1x3.setIcon(icon21)
                self.dispositionButton_1x3.setIconSize(QtCore.QSize(40, 40))
                self.dispositionButton_1x3.setObjectName("dispositionButton_1x3")
                self.dispositionButton_1x3.setToolTip("Mostrar disposición 1x3 (Sagital) (Axial) (Coronal)")
                self.dispositionButton_1x3.clicked.connect(self.display_three_images_horizontal)
                self.dispositionButton_1x3.setCheckable(True)
                self.gridLayout_7.addWidget(self.dispositionButton_1x3, 0, 2, 1, 1)
                self.dispositionButton_1x2 = QtWidgets.QPushButton(self.gridLayoutWidget_7)
                self.dispositionButton_1x2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                icon22 = QtGui.QIcon()
                icon22.addPixmap(QtGui.QPixmap(".\\Assets/1x2grid.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.dispositionButton_1x2.setIcon(icon22)
                self.dispositionButton_1x2.setIconSize(QtCore.QSize(40, 40))
                self.dispositionButton_1x2.setObjectName("dispositionButton_1x2")
                self.dispositionButton_1x2.setToolTip("Mostrar disposición 1x2 (Sagital) izquierda (Axial) derecha")
                self.dispositionButton_1x2.clicked.connect(self.display_two_images_horizontal)
                self.dispositionButton_1x2.setCheckable(True)
                self.gridLayout_7.addWidget(self.dispositionButton_1x2, 0, 1, 1, 1)
                self.dispositionButton_1u2d = QtWidgets.QPushButton(self.gridLayoutWidget_7)
                self.dispositionButton_1u2d.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                icon23 = QtGui.QIcon()
                icon23.addPixmap(QtGui.QPixmap(".\\Assets/1up_2downgrid.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.dispositionButton_1u2d.setIcon(icon23)
                self.dispositionButton_1u2d.setIconSize(QtCore.QSize(45, 45))
                self.dispositionButton_1u2d.setObjectName("dispositionButton_1u2d")
                self.dispositionButton_1u2d.setToolTip("Mostrar disposición (Sagital) arriba y (Axial y Coronal) abajo")
                self.dispositionButton_1u2d.clicked.connect(self.display_three_images_t)
                self.dispositionButton_1u2d.setCheckable(True)
                self.gridLayout_7.addWidget(self.dispositionButton_1u2d, 1, 0, 1, 1)
                self.dispositionButton_1l2r = QtWidgets.QPushButton(self.gridLayoutWidget_7)
                self.dispositionButton_1l2r.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                icon24 = QtGui.QIcon()
                icon24.addPixmap(QtGui.QPixmap(".\\Assets/1+2grid.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.dispositionButton_1l2r.setIcon(icon24)
                self.dispositionButton_1l2r.setIconSize(QtCore.QSize(45, 45))
                self.dispositionButton_1l2r.setObjectName("dispositionButton_1l2r")
                self.dispositionButton_1l2r.setToolTip("Mostrar disposición (Sagital) izquierda y (Axial y Coronal) derecha")
                self.dispositionButton_1l2r.clicked.connect(self.display_three_images_inverted_t)
                self.dispositionButton_1l2r.setCheckable(True)
                self.gridLayout_7.addWidget(self.dispositionButton_1l2r, 1, 2, 1, 1)
                self.label_14 = QtWidgets.QLabel(self.frame_22)
                self.label_14.setGeometry(QtCore.QRect(40, 0, 171, 31))
                self.label_14.setStyleSheet("font: 87 16pt \"Roboto\" \"bold\";\n"
                "background-color: rgb(119, 118, 179);\n"
                "color:#FFFFFF;\n"
                "border-radius: 15px;")
                self.label_14.setTextFormat(QtCore.Qt.PlainText)
                self.label_14.setAlignment(QtCore.Qt.AlignCenter)
                self.label_14.setObjectName("label_14")
                self.verticalLayout_4.addWidget(self.frame_22)
                spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                self.verticalLayout_4.addItem(spacerItem2)
                self.stackedWidget_submenuVisualizacion.addWidget(self.submenuTools)
                self.verticalLayout.addWidget(self.stackedWidget_submenuVisualizacion)
                self.horizontalLayout_5.addWidget(self.frame_2)
                self.frame_3 = QtWidgets.QWidget(self.pantallaVisualizacion)
                self.frame_3.setMinimumSize(QtCore.QSize(1100, 0))
                self.frame_3.setMaximumSize(QtCore.QSize(16777215, 16777215))
                self.frame_3.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
                self.frame_3.setObjectName("frame_3")
                self.central_layout = QtWidgets.QHBoxLayout(self.frame_3)
                self.frame_3.setLayout(self.central_layout)
                self.horizontalLayout_5.addWidget(self.frame_3)
                self.stackedWidgetPrincipal.addWidget(self.pantallaVisualizacion)
                self.pantallaBaseDeDatos = QtWidgets.QWidget()
                self.pantallaBaseDeDatos.setStyleSheet("background-color: rgb(255, 255, 255);")
                self.pantallaBaseDeDatos.setObjectName("pantallaBaseDeDatos")
                self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.pantallaBaseDeDatos)
                self.verticalLayout_6.setObjectName("verticalLayout_6")
                self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
                self.horizontalLayout_7.setObjectName("horizontalLayout_7")
                self.filterLiner_db = QtWidgets.QLineEdit(self.pantallaBaseDeDatos)
                self.filterLiner_db.setMaximumSize(QtCore.QSize(300, 16777215))
                self.filterLiner_db.setStyleSheet("border: 1px solid #A0A0A0;\n"
                "border-radius: 5px;\n"
                "padding: 2px;\n"
                "background-color: white;")
                self.filterLiner_db.setObjectName("filterLiner_db")
                self.horizontalLayout_7.addWidget(self.filterLiner_db)
                spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
                self.horizontalLayout_7.addItem(spacerItem3)
                self.label_3 = QtWidgets.QLabel(self.pantallaBaseDeDatos)
                self.label_3.setMinimumSize(QtCore.QSize(0, 70))
                font = QtGui.QFont()
                font.setFamily("Roboto")
                font.setPointSize(36)
                font.setBold(True)
                font.setWeight(75)
                self.label_3.setFont(font)
                self.label_3.setAlignment(QtCore.Qt.AlignCenter)
                self.label_3.setObjectName("label_3")
                self.horizontalLayout_7.addWidget(self.label_3)
                spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
                self.horizontalLayout_7.addItem(spacerItem4)
                self.verticalLayout_6.addLayout(self.horizontalLayout_7)
                self.database_table = QtWidgets.QTableWidget(self.pantallaBaseDeDatos)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.database_table.sizePolicy().hasHeightForWidth())
                self.database_table.setSizePolicy(sizePolicy)
                self.database_table.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
                self.database_table.setAutoFillBackground(False)
                self.database_table.setStyleSheet("QTableWidget {\n"
                "    font-family: \'Roboto\', sans-serif;\n"
                "\n"
                "    border-radius: 10px;\n"
                "    gridline-color: #D9D9D9;\n"
                "    border: none;\n"
                "}\n"
                "\n"
                "QHeaderView::section {\n"
                "    background-color: #5A639C;\n"
                "    color: white;\n"
                "    font-weight: bold;\n"
                "    font-size: 20px;\n"
                "    padding: 5px;\n"
                "    border: none;\n"
                "    text-align: center;\n"
                "}\n"
                "\n"
                "QTableWidget::item {\n"
                "    color: black;\n"
                "    font-weight: regular;\n"
                "    background-color: #D9D9D9;\n"
                "    font-size: 16px;\n"
                "    padding: 5px;\n"
                "    text-align: center;\n"
                "    border: none;\n"
                "}\n"
                "\n"
                "QTableWidget::item:selected {\n"
                "    background-color: #B0B0B0;\n"
                "}\n"
                "\n"
                "/* Centrar verticalmente el contenido de las celdas */\n"
                "QTableWidget::item {\n"
                "    padding-top: 5px;\n"
                "    padding-bottom: 5px;\n"
                "}\n"
                "\n"
                "/* Asegurar que el texto se centre horizontalmente */\n"
                "QTableWidget {\n"
                "    qproperty-textElideMode: ElideNone;\n"
                "    qproperty-showGrid: false;\n"
                "}\n"
                "\n"
                "/* Estilo para el viewport del QTableWidget */\n"
                "QTableWidget QTableCornerButton::section {\n"
                "    background-color: #5A639C;\n"
                "    border: none;\n"
                "}\n"
                "\n"
                "QScrollBar:horizontal,\n"
                "QScrollBar:vertical {\n"
                "    background-color: #D9D9D9;\n"
                "    border-radius: 5px;\n"
                "    margin: 0px;\n"
                "}\n"
                "\n"
                "QScrollBar::handle:horizontal,\n"
                "QScrollBar::handle:vertical {\n"
                "    background-color: #5A639C;\n"
                "    border-radius: 5px;\n"
                "    min-height: 2px;\n"
                "    min-width: 2px;\n"
                "}\n"
                "\n"
                "QScrollBar::add-line:horizontal,\n"
                "QScrollBar::sub-line:horizontal,\n"
                "QScrollBar::add-line:vertical,\n"
                "QScrollBar::sub-line:vertical {\n"
                "    border: none;\n"
                "    background: none;\n"
                "    width: 0px;\n"
                "    height: 0px;\n"
                "}\n"
                "\n"
                "QScrollBar::add-page:horizontal,\n"
                "QScrollBar::sub-page:horizontal,\n"
                "QScrollBar::add-page:vertical,\n"
                "QScrollBar::sub-page:vertical {\n"
                "    background: none;\n"
                "}\n"
                "\n"
                "QScrollBar::handle:vertical {\n"
                "    max-height: 10px;\n"
                "    min-height: 8px;\n"
                "}")
                self.database_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
                self.database_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                self.database_table.setShowGrid(False)
                self.database_table.setCornerButtonEnabled(False)
                self.database_table.setObjectName("database_table")
                self.database_table.setColumnCount(6)
                self.database_table.setRowCount(0)
                item = QtWidgets.QTableWidgetItem()
                self.database_table.setHorizontalHeaderItem(0, item)
                item = QtWidgets.QTableWidgetItem()
                self.database_table.setHorizontalHeaderItem(1, item)
                item = QtWidgets.QTableWidgetItem()
                self.database_table.setHorizontalHeaderItem(2, item)
                item = QtWidgets.QTableWidgetItem()
                self.database_table.setHorizontalHeaderItem(3, item)
                item = QtWidgets.QTableWidgetItem()
                self.database_table.setHorizontalHeaderItem(4, item)
                item = QtWidgets.QTableWidgetItem()
                icon25 = QtGui.QIcon()
                icon25.addPixmap(QtGui.QPixmap(".\\Assets/trash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                item.setIcon(icon25)
                self.database_table.setHorizontalHeaderItem(5, item)
                self.verticalLayout_6.addWidget(self.database_table)
                self.stackedWidgetPrincipal.addWidget(self.pantallaBaseDeDatos)
                self.pantallaAnadirArchivo = QtWidgets.QWidget()
                self.pantallaAnadirArchivo.setStyleSheet("\n"
                "background-color: rgb(255, 255, 255);")
                self.pantallaAnadirArchivo.setObjectName("pantallaAnadirArchivo")
                self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.pantallaAnadirArchivo)
                self.horizontalLayout_2.setObjectName("horizontalLayout_2")
                self.verticalLayout_5 = QtWidgets.QVBoxLayout()
                self.verticalLayout_5.setObjectName("verticalLayout_5")
                spacerItem5 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
                self.verticalLayout_5.addItem(spacerItem5)
                self.label = QtWidgets.QLabel(self.pantallaAnadirArchivo)
                self.label.setMaximumSize(QtCore.QSize(16777215, 50))
                palette = QtGui.QPalette()
                brush = QtGui.QBrush(QtGui.QColor(90, 99, 156))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
                brush = QtGui.QBrush(QtGui.QColor(90, 99, 156))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
                brush = QtGui.QBrush(QtGui.QColor(90, 99, 156))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
                brush = QtGui.QBrush(QtGui.QColor(90, 99, 156))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
                brush = QtGui.QBrush(QtGui.QColor(90, 99, 156))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
                brush = QtGui.QBrush(QtGui.QColor(90, 99, 156))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
                brush = QtGui.QBrush(QtGui.QColor(90, 99, 156))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
                brush = QtGui.QBrush(QtGui.QColor(90, 99, 156))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
                brush = QtGui.QBrush(QtGui.QColor(90, 99, 156))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
                self.label.setPalette(palette)
                font = QtGui.QFont()
                font.setFamily("Roboto")
                font.setPointSize(24)
                font.setBold(True)
                font.setWeight(75)
                self.label.setFont(font)
                self.label.setStyleSheet("color:#5A639C")
                self.label.setAlignment(QtCore.Qt.AlignCenter)
                self.label.setObjectName("label")
                self.verticalLayout_5.addWidget(self.label)
                spacerItem6 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
                self.verticalLayout_5.addItem(spacerItem6)
                self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
                self.horizontalLayout_3.setObjectName("horizontalLayout_3")
                self.frame_24 = QtWidgets.QFrame(self.pantallaAnadirArchivo)
                self.frame_24.setMinimumSize(QtCore.QSize(0, 400))
                self.frame_24.setMaximumSize(QtCore.QSize(16777215, 2000))
                self.frame_24.setStyleSheet("background-color: #E8C9ED;\n"
                "border-radius: 15px;")
                self.frame_24.setFrameShape(QtWidgets.QFrame.NoFrame)
                self.frame_24.setObjectName("frame_24")
                self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_24)
                self.verticalLayout_7.setObjectName("verticalLayout_7")
                self.frame_25 = QtWidgets.QFrame(self.frame_24)
                self.frame_25.setMinimumSize(QtCore.QSize(10, 0))
                self.frame_25.setMaximumSize(QtCore.QSize(16777215, 1000))
                self.frame_25.setStyleSheet("border: 2px dashed #5A639C;\n"
                "border-radius: 15px;")
                self.frame_25.setFrameShape(QtWidgets.QFrame.NoFrame)
                self.frame_25.setObjectName("frame_25")
                self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_25)
                self.gridLayout_2.setObjectName("gridLayout_2")
                spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
                self.gridLayout_2.addItem(spacerItem7, 0, 0, 1, 1)
                self.pushButton = QtWidgets.QPushButton(self.frame_25)
                self.pushButton.setStyleSheet("border: 2px dashed #E8C9ED;")
                self.pushButton.setText("")
                icon26 = QtGui.QIcon()
                icon26.addPixmap(QtGui.QPixmap(":/icons/Assets/icon_documentUpload.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.pushButton.setIcon(icon26)
                self.pushButton.setIconSize(QtCore.QSize(160, 160))
                self.pushButton.setObjectName("pushButton")
                self.gridLayout_2.addWidget(self.pushButton, 1, 0, 1, 1)
                self.label_2 = QtWidgets.QLabel(self.frame_25)
                font = QtGui.QFont()
                font.setFamily("Roboto")
                font.setBold(True)
                font.setWeight(75)
                self.label_2.setFont(font)
                self.label_2.setStyleSheet("border: 2px dashed #E8C9ED;")
                self.label_2.setAlignment(QtCore.Qt.AlignCenter)
                self.label_2.setObjectName("label_2")
                self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
                spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
                self.gridLayout_2.addItem(spacerItem8, 3, 0, 1, 1)
                self.verticalLayout_7.addWidget(self.frame_25)
                self.horizontalLayout_3.addWidget(self.frame_24)
                self.verticalLayout_5.addLayout(self.horizontalLayout_3)
                spacerItem9 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
                self.verticalLayout_5.addItem(spacerItem9)
                self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
                self.horizontalLayout_4.setObjectName("horizontalLayout_4")
                spacerItem10 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
                self.horizontalLayout_4.addItem(spacerItem10)
                self.archivoButton_carpeta = QtWidgets.QPushButton(self.pantallaAnadirArchivo)
                self.archivoButton_carpeta.setMinimumSize(QtCore.QSize(200, 50))
                font = QtGui.QFont()
                font.setFamily("Roboto")
                font.setPointSize(12)
                font.setBold(True)
                font.setWeight(75)
                self.archivoButton_carpeta.setFont(font)
                self.archivoButton_carpeta.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.archivoButton_carpeta.setStyleSheet("background-color: rgb(90, 99, 156);\n"
                "color:#ffffff;\n"
                "border-radius:15px;")
                self.archivoButton_carpeta.setObjectName("archivoButton_carpeta")
                self.horizontalLayout_4.addWidget(self.archivoButton_carpeta)
                spacerItem11 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
                self.horizontalLayout_4.addItem(spacerItem11)
                self.verticalLayout_5.addLayout(self.horizontalLayout_4)
                self.horizontalLayout_2.addLayout(self.verticalLayout_5)
                self.stackedWidgetPrincipal.addWidget(self.pantallaAnadirArchivo)
                self.horizontalLayout.addWidget(self.stackedWidgetPrincipal)
                self.viewer_actions = ViewerActions(self.frame_3, self.dcm_viewer, viewers, self.ViewersConnection, self.vtkBaseClass)
                MainWindow.setCentralWidget(self.centralwidget)

                #Listas de botones
                self.view_buttons = [self.dispositionButton_2x2, 
                                     self.dispositionButton_1x1, 
                                     self.dispositionButton_2x1, 
                                     self.dispositionButton_1x3, 
                                     self.dispositionButton_1x2, 
                                     self.dispositionButton_1u2d, 
                                     self.dispositionButton_1l2r]
                self.tools_buttons = [self.toolButton_filtros,
                                      self.toolButton_regla,
                                      self.toolButton_areaCircular,
                                      self.toolButton_flechas,
                                      self.toolButton_dibujoLibre,
                                      self.toolButton_angulos,
                                      self.toolButton_descargaImagen,
                                      self.toolButton_borrador,
                                      self.toolButton_areaRectangular,
                                      self.toolButton_escritura,
                                      self.functionButton_brillo,
                                      self.functionButton_rotacion,
                                      self.functionButton_desplazamiento,
                                      self.toolButton_borrador]
                #Inicializa los botones como inhabilitados hasta que no se seleccione un estudio
                self.set_enabled_views(False)
                self.set_enabled_tools(False)

                #Cambio de apariencia en los botones cuando son presionados
                self.set_stylesheet()
                
                
        def display_one_image(self):
                self.uncheck_views()
                self.dispositionButton_1x1.setChecked(True)
                self.set_enabled_tools(True)
                self.viewer_actions.display_one_image()

        def display_two_images_vertical(self):
                self.uncheck_views()
                self.dispositionButton_2x1.setChecked(True)
                self.set_enabled_tools(True)
                self.viewer_actions.display_two_images_vertical()

        def display_two_images_horizontal(self):
                self.uncheck_views()
                self.dispositionButton_1x2.setChecked(True)
                self.set_enabled_tools(True)
                self.viewer_actions.display_two_images_horizontal()

        def display_three_images_horizontal(self):
                self.uncheck_views()
                self.dispositionButton_1x3.setChecked(True)
                self.set_enabled_tools(True)
                self.viewer_actions.display_three_images_horizontal()

        def display_three_images_t(self):
                self.uncheck_views()
                self.dispositionButton_1u2d.setChecked(True)
                self.set_enabled_tools(True)
                self.viewer_actions.display_three_images_t()

        def display_three_images_inverted_t(self):
                self.uncheck_views()
                self.dispositionButton_1l2r.setChecked(True)
                self.set_enabled_tools(True)
                self.viewer_actions.display_three_images_inverted_t()

        def display_four_images(self):
                self.uncheck_views()
                self.dispositionButton_2x2.setChecked(True)
                self.set_enabled_tools(True)
                self.viewer_actions.display_four_images()

        def activate_distance_measurement(self):
                self.viewer_actions.activate_distance_measurement()
               
        def set_canvas(self):
                self.viewer_actions.set_canvas()
        
        def set_shape_canvas(self,shape):
                self.viewer_actions.set_shape_canvas(shape)

        def set_text_canvas(self):
                self.viewer_actions.set_text_canvas()

        def clear_canvas_drawing(self):
                self.viewer_actions.clear_canvas_drawing()
                
        def uncheck_views(self):
                for button in self.view_buttons:
                        button.setChecked(False)
        
        def uncheck_tools(self):
                for button in self.tools_buttons:
                        button.setChecked(False)
        
        #TODO: implement
        def reset_tools(self):
                if self.canvas is not None:
                        self.viewer_actions.set_canvas()
                
        def set_enabled_views(self, enabled: bool):
                for button in self.view_buttons:
                        button.setEnabled(enabled)

        def set_enabled_tools(self, enabled: bool):
                for button in self.tools_buttons:
                        button.setEnabled(enabled)
        
        def set_stylesheet(self):
                for button in self.view_buttons:
                        button.setStyleSheet("""
                                        QPushButton:checked {
                                                background-color: #a0a0a0; /* Color de fondo al presionar */
                                                border: 2px solid #808080; /* Bordes al presionar */
                                        }
                                        QPushButton:pressed {
                                                background-color: #a0a0a0; /* Color de fondo al presionar */
                                                border: 2px solid #808080; /* Bordes al presionar */
                                        }
                                        QPushButton:hover {
                                                background-color: #e599f7;  /* Fondo más oscuro al pasar el mouse */
                                        }
                                        """)
                for button in self.tools_buttons:
                        button.setStyleSheet("""
                                        QPushButton:checked {
                                                background-color: #a0a0a0; /* Color de fondo al presionar */
                                                border: 2px solid #808080; /* Bordes al presionar */
                                        }
                                        QPushButton:pressed {
                                                background-color: #a0a0a0; /* Color de fondo al presionar */
                                                border: 2px solid #808080; /* Bordes al presionar */
                                        }
                                        QPushButton:hover {
                                                background-color: #e599f7;  /* Fondo más oscuro al pasar el mouse */
                                        }
                                        """)

        def clear_layout(self):
                self.viewer_actions.clear_layout()

        def hide_studies(self):
                self.viewer_actions.hide_studies()

        def retranslateUi(self, MainWindow):
                _translate = QtCore.QCoreApplication.translate
                MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
                self.subMenu_tools.setShortcut(_translate("MainWindow", "Esc"))
                item = self.patientInfo_table.horizontalHeaderItem(0)
                item.setText(_translate("MainWindow", "Campo"))
                item = self.patientInfo_table.horizontalHeaderItem(1)
                item.setText(_translate("MainWindow", "Valor"))
                self.label_9.setText(_translate("MainWindow", "Paciente"))
                item = self.studyInfo_table.horizontalHeaderItem(0)
                item.setText(_translate("MainWindow", "Campo"))
                item = self.studyInfo_table.horizontalHeaderItem(1)
                item.setText(_translate("MainWindow", "Valor"))
                self.label_11.setText(_translate("MainWindow", "Estudio"))
                self.label_8.setText(_translate("MainWindow", "Herramientas"))
                self.label_10.setText(_translate("MainWindow", "Funciones"))
                self.label_14.setText(_translate("MainWindow", "Disposición"))
                self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5a639c;\">Base de Datos</span></p></body></html>"))
                item = self.database_table.horizontalHeaderItem(0)
                item.setText(_translate("MainWindow", "Nombre"))
                item = self.database_table.horizontalHeaderItem(1)
                item.setText(_translate("MainWindow", "ID - Paciente"))
                item = self.database_table.horizontalHeaderItem(2)
                item.setText(_translate("MainWindow", "Sexo"))
                item = self.database_table.horizontalHeaderItem(3)
                item.setText(_translate("MainWindow", "Fecha Nac."))
                item = self.database_table.horizontalHeaderItem(4)
                item.setText(_translate("MainWindow", "Modalidades"))
                self.label.setText(_translate("MainWindow", "Carga de Archivos"))
                self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:20pt; color:#5a639c;\">Arrastre y suelte los archivos </span></p><p><span style=\" font-size:20pt; color:#5a639c;\">DICOM acá</span></p></body></html>"))
                self.archivoButton_carpeta.setText(_translate("MainWindow", "Seleccionar carpeta"))
import resources_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
