# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ventana1.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QVBoxLayout, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1065, 700)
        MainWindow.setMinimumSize(QSize(800, 600))
        MainWindow.setMaximumSize(QSize(1920, 1080))
        MainWindow.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(70, 0))
        self.frame.setMaximumSize(QSize(70, 16777215))
        self.frame.setStyleSheet(u"background-color:rgb(90, 99, 156)")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_9 = QFrame(self.frame)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.NoFrame)

        self.verticalLayout_2.addWidget(self.frame_9)

        self.frame_10 = QFrame(self.frame)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setStyleSheet(u"QPushButton{\n"
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
        self.frame_10.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_3 = QVBoxLayout(self.frame_10)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.mainButton_DB = QPushButton(self.frame_10)
        self.mainButton_DB.setObjectName(u"mainButton_DB")
        self.mainButton_DB.setMinimumSize(QSize(50, 50))
        self.mainButton_DB.setMaximumSize(QSize(50, 50))
        self.mainButton_DB.setStyleSheet(u"border:0px;")
        icon = QIcon()
        icon.addFile(u"Assets/database_white.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.mainButton_DB.setIcon(icon)
        self.mainButton_DB.setIconSize(QSize(50, 50))
        self.mainButton_DB.setCheckable(True)
        self.mainButton_DB.setAutoExclusive(True)

        self.verticalLayout_3.addWidget(self.mainButton_DB)

        self.mainButton_visualizacion = QPushButton(self.frame_10)
        self.mainButton_visualizacion.setObjectName(u"mainButton_visualizacion")
        self.mainButton_visualizacion.setMinimumSize(QSize(50, 50))
        self.mainButton_visualizacion.setMaximumSize(QSize(50, 50))
        icon1 = QIcon()
        icon1.addFile(u":/icons/Assets/display_white.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.mainButton_visualizacion.setIcon(icon1)
        self.mainButton_visualizacion.setIconSize(QSize(4000, 50))
        self.mainButton_visualizacion.setCheckable(True)
        self.mainButton_visualizacion.setChecked(True)
        self.mainButton_visualizacion.setAutoExclusive(True)

        self.verticalLayout_3.addWidget(self.mainButton_visualizacion)

        self.mainButton_anadirArchivo = QPushButton(self.frame_10)
        self.mainButton_anadirArchivo.setObjectName(u"mainButton_anadirArchivo")
        self.mainButton_anadirArchivo.setMinimumSize(QSize(50, 50))
        self.mainButton_anadirArchivo.setMaximumSize(QSize(50, 50))
        self.mainButton_anadirArchivo.setStyleSheet(u"border:0px;")
        icon2 = QIcon()
        icon2.addFile(u"Assets/addDicom_white.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.mainButton_anadirArchivo.setIcon(icon2)
        self.mainButton_anadirArchivo.setIconSize(QSize(50, 50))
        self.mainButton_anadirArchivo.setCheckable(True)
        self.mainButton_anadirArchivo.setAutoExclusive(True)

        self.verticalLayout_3.addWidget(self.mainButton_anadirArchivo)


        self.verticalLayout_2.addWidget(self.frame_10)

        self.frame_11 = QFrame(self.frame)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.NoFrame)

        self.verticalLayout_2.addWidget(self.frame_11)


        self.horizontalLayout.addWidget(self.frame)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.pantallaVisualizacion = QWidget()
        self.pantallaVisualizacion.setObjectName(u"pantallaVisualizacion")
        self.pantallaVisualizacion.setStyleSheet(u"\n"
"background-color: rgb(0, 0, 0);")
        self.horizontalLayout_5 = QHBoxLayout(self.pantallaVisualizacion)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.pantallaVisualizacion)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMaximumSize(QSize(270, 16777215))
        self.frame_2.setStyleSheet(u"background-color: rgb(255, 255, 255)")
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.verticalLayout = QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 0, -1, -1)
        self.frame_17 = QFrame(self.frame_2)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setMinimumSize(QSize(250, 70))
        self.frame_17.setMaximumSize(QSize(250, 70))
        self.frame_17.setStyleSheet(u"background-color: #5A639C;\n"
"border-radius: 30px;")
        self.frame_17.setFrameShape(QFrame.NoFrame)

        self.verticalLayout.addWidget(self.frame_17)

        self.verticalSpacer_2 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.frame_12 = QFrame(self.frame_2)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setMinimumSize(QSize(200, 190))
        self.frame_12.setMaximumSize(QSize(16777215, 190))
        self.frame_12.setStyleSheet(u"background-color: #FFFFFF;\n"
"\n"
"")
        self.frame_12.setFrameShape(QFrame.NoFrame)
        self.frame_13 = QFrame(self.frame_12)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setGeometry(QRect(0, 20, 250, 161))
        self.frame_13.setMinimumSize(QSize(250, 0))
        self.frame_13.setMaximumSize(QSize(250, 200))
        self.frame_13.setStyleSheet(u"background-color: #E8C9ED;\n"
"border-radius: 15px;")
        self.frame_13.setFrameShape(QFrame.NoFrame)
        self.gridLayoutWidget = QWidget(self.frame_13)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(0, 10, 251, 154))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.toolButton_filtros = QPushButton(self.gridLayoutWidget)
        self.toolButton_filtros.setObjectName(u"toolButton_filtros")
        icon3 = QIcon()
        icon3.addFile(u"Assets/colorfilter.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.toolButton_filtros.setIcon(icon3)
        self.toolButton_filtros.setIconSize(QSize(40, 40))

        self.gridLayout.addWidget(self.toolButton_filtros, 0, 2, 1, 1)

        self.toolButton_regla = QPushButton(self.gridLayoutWidget)
        self.toolButton_regla.setObjectName(u"toolButton_regla")
        icon4 = QIcon()
        icon4.addFile(u":/icons/Assets/ruler.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.toolButton_regla.setIcon(icon4)
        self.toolButton_regla.setIconSize(QSize(40, 40))

        self.gridLayout.addWidget(self.toolButton_regla, 0, 0, 1, 1)

        self.toolButton_areaCircular = QPushButton(self.gridLayoutWidget)
        self.toolButton_areaCircular.setObjectName(u"toolButton_areaCircular")
        icon5 = QIcon()
        icon5.addFile(u"Assets/Ellipse.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.toolButton_areaCircular.setIcon(icon5)
        self.toolButton_areaCircular.setIconSize(QSize(45, 45))

        self.gridLayout.addWidget(self.toolButton_areaCircular, 1, 0, 1, 1)

        self.toolButton_flechas = QPushButton(self.gridLayoutWidget)
        self.toolButton_flechas.setObjectName(u"toolButton_flechas")
        icon6 = QIcon()
        icon6.addFile(u"Assets/Arrow 1.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.toolButton_flechas.setIcon(icon6)
        self.toolButton_flechas.setIconSize(QSize(35, 35))

        self.gridLayout.addWidget(self.toolButton_flechas, 1, 3, 1, 1)

        self.toolButton_dibujoLibre = QPushButton(self.gridLayoutWidget)
        self.toolButton_dibujoLibre.setObjectName(u"toolButton_dibujoLibre")
        icon7 = QIcon()
        icon7.addFile(u"Assets/freeDraw.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.toolButton_dibujoLibre.setIcon(icon7)
        self.toolButton_dibujoLibre.setIconSize(QSize(40, 40))

        self.gridLayout.addWidget(self.toolButton_dibujoLibre, 0, 1, 1, 1)

        self.toolButton_angulos = QPushButton(self.gridLayoutWidget)
        self.toolButton_angulos.setObjectName(u"toolButton_angulos")
        icon8 = QIcon()
        icon8.addFile(u"Assets/Angle.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.toolButton_angulos.setIcon(icon8)
        self.toolButton_angulos.setIconSize(QSize(40, 40))

        self.gridLayout.addWidget(self.toolButton_angulos, 1, 2, 1, 1)

        self.toolButton_descargaImagen = QPushButton(self.gridLayoutWidget)
        self.toolButton_descargaImagen.setObjectName(u"toolButton_descargaImagen")
        icon9 = QIcon()
        icon9.addFile(u"Assets/gallery-import.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.toolButton_descargaImagen.setIcon(icon9)
        self.toolButton_descargaImagen.setIconSize(QSize(45, 40))

        self.gridLayout.addWidget(self.toolButton_descargaImagen, 2, 1, 1, 1)

        self.toolButton_borrador = QPushButton(self.gridLayoutWidget)
        self.toolButton_borrador.setObjectName(u"toolButton_borrador")
        icon10 = QIcon()
        icon10.addFile(u"Assets/eraser.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.toolButton_borrador.setIcon(icon10)
        self.toolButton_borrador.setIconSize(QSize(45, 45))

        self.gridLayout.addWidget(self.toolButton_borrador, 2, 0, 1, 1)

        self.toolButton_areaRectangular = QPushButton(self.gridLayoutWidget)
        self.toolButton_areaRectangular.setObjectName(u"toolButton_areaRectangular")
        icon11 = QIcon()
        icon11.addFile(u"Assets/Rectangle 20.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.toolButton_areaRectangular.setIcon(icon11)
        self.toolButton_areaRectangular.setIconSize(QSize(40, 40))

        self.gridLayout.addWidget(self.toolButton_areaRectangular, 1, 1, 1, 1)

        self.toolButton_escritura = QPushButton(self.gridLayoutWidget)
        self.toolButton_escritura.setObjectName(u"toolButton_escritura")
        icon12 = QIcon()
        icon12.addFile(u"Assets/A.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.toolButton_escritura.setIcon(icon12)
        self.toolButton_escritura.setIconSize(QSize(35, 35))

        self.gridLayout.addWidget(self.toolButton_escritura, 0, 3, 1, 1)

        self.label_8 = QLabel(self.frame_12)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(40, 0, 171, 31))
        self.label_8.setStyleSheet(u"font: 87 16pt \"Roboto\" \"bold\";\n"
"background-color: rgb(119, 118, 179);\n"
"color:#FFFFFF;\n"
"border-radius: 15px;")
        self.label_8.setTextFormat(Qt.PlainText)
        self.label_8.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.frame_12)

        self.frame_14 = QFrame(self.frame_2)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setMinimumSize(QSize(250, 100))
        self.frame_14.setMaximumSize(QSize(16777215, 100))
        self.frame_14.setStyleSheet(u"background-color: #FFFFFF;\n"
"\n"
"")
        self.frame_14.setFrameShape(QFrame.NoFrame)
        self.frame_16 = QFrame(self.frame_14)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setGeometry(QRect(0, 20, 250, 71))
        self.frame_16.setMinimumSize(QSize(0, 0))
        self.frame_16.setMaximumSize(QSize(250, 200))
        self.frame_16.setStyleSheet(u"background-color: #E8C9ED;\n"
"border-radius: 15px;")
        self.frame_16.setFrameShape(QFrame.NoFrame)
        self.gridLayoutWidget_3 = QWidget(self.frame_16)
        self.gridLayoutWidget_3.setObjectName(u"gridLayoutWidget_3")
        self.gridLayoutWidget_3.setGeometry(QRect(0, 10, 251, 61))
        self.gridLayout_3 = QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(0)
        self.gridLayout_3.setContentsMargins(5, 5, 5, 5)
        self.functionButton_brillo = QPushButton(self.gridLayoutWidget_3)
        self.functionButton_brillo.setObjectName(u"functionButton_brillo")
        icon13 = QIcon()
        icon13.addFile(u"Assets/brightness.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.functionButton_brillo.setIcon(icon13)
        self.functionButton_brillo.setIconSize(QSize(40, 40))

        self.gridLayout_3.addWidget(self.functionButton_brillo, 0, 2, 1, 1)

        self.functionButton_rotacion = QPushButton(self.gridLayoutWidget_3)
        self.functionButton_rotacion.setObjectName(u"functionButton_rotacion")
        icon14 = QIcon()
        icon14.addFile(u"Assets/refresh-circle.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.functionButton_rotacion.setIcon(icon14)
        self.functionButton_rotacion.setIconSize(QSize(50, 50))

        self.gridLayout_3.addWidget(self.functionButton_rotacion, 0, 1, 1, 1)

        self.functionButton_desplazamiento = QPushButton(self.gridLayoutWidget_3)
        self.functionButton_desplazamiento.setObjectName(u"functionButton_desplazamiento")
        icon15 = QIcon()
        icon15.addFile(u"Assets/displacement.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.functionButton_desplazamiento.setIcon(icon15)
        self.functionButton_desplazamiento.setIconSize(QSize(50, 50))

        self.gridLayout_3.addWidget(self.functionButton_desplazamiento, 0, 0, 1, 1)

        self.label_10 = QLabel(self.frame_14)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(40, 0, 171, 31))
        self.label_10.setStyleSheet(u"font: 87 16pt \"Roboto\" \"bold\";\n"
"background-color: rgb(119, 118, 179);\n"
"color:#FFFFFF;\n"
"border-radius: 15px;")
        self.label_10.setTextFormat(Qt.PlainText)
        self.label_10.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.frame_14)

        self.frame_22 = QFrame(self.frame_2)
        self.frame_22.setObjectName(u"frame_22")
        self.frame_22.setMinimumSize(QSize(0, 160))
        self.frame_22.setMaximumSize(QSize(16777215, 225))
        self.frame_22.setStyleSheet(u"background-color: #FFFFFF;\n"
"\n"
"")
        self.frame_22.setFrameShape(QFrame.NoFrame)
        self.frame_23 = QFrame(self.frame_22)
        self.frame_23.setObjectName(u"frame_23")
        self.frame_23.setGeometry(QRect(0, 20, 250, 131))
        self.frame_23.setMinimumSize(QSize(250, 0))
        self.frame_23.setMaximumSize(QSize(250, 200))
        self.frame_23.setStyleSheet(u"background-color: #E8C9ED;\n"
"border-radius: 15px;")
        self.frame_23.setFrameShape(QFrame.NoFrame)
        self.gridLayoutWidget_7 = QWidget(self.frame_23)
        self.gridLayoutWidget_7.setObjectName(u"gridLayoutWidget_7")
        self.gridLayoutWidget_7.setGeometry(QRect(0, 10, 251, 121))
        self.gridLayout_7 = QGridLayout(self.gridLayoutWidget_7)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setHorizontalSpacing(0)
        self.gridLayout_7.setContentsMargins(5, 5, 5, 5)
        self.dispositionButton_2x2 = QPushButton(self.gridLayoutWidget_7)
        self.dispositionButton_2x2.setObjectName(u"dispositionButton_2x2")
        icon16 = QIcon()
        icon16.addFile(u"Assets/2x2 grid.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.dispositionButton_2x2.setIcon(icon16)
        self.dispositionButton_2x2.setIconSize(QSize(45, 45))

        self.gridLayout_7.addWidget(self.dispositionButton_2x2, 1, 1, 1, 1)

        self.dispositionButton_1x1 = QPushButton(self.gridLayoutWidget_7)
        self.dispositionButton_1x1.setObjectName(u"dispositionButton_1x1")
        icon17 = QIcon()
        icon17.addFile(u"Assets/Rectangle 24.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.dispositionButton_1x1.setIcon(icon17)
        self.dispositionButton_1x1.setIconSize(QSize(45, 45))

        self.gridLayout_7.addWidget(self.dispositionButton_1x1, 0, 0, 1, 1)

        self.dispositionButton_2x1 = QPushButton(self.gridLayoutWidget_7)
        self.dispositionButton_2x1.setObjectName(u"dispositionButton_2x1")
        icon18 = QIcon()
        icon18.addFile(u"Assets/2x1grid.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.dispositionButton_2x1.setIcon(icon18)
        self.dispositionButton_2x1.setIconSize(QSize(35, 35))

        self.gridLayout_7.addWidget(self.dispositionButton_2x1, 0, 3, 1, 1)

        self.dispositionButton_1x3 = QPushButton(self.gridLayoutWidget_7)
        self.dispositionButton_1x3.setObjectName(u"dispositionButton_1x3")
        icon19 = QIcon()
        icon19.addFile(u"Assets/1x3grid.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.dispositionButton_1x3.setIcon(icon19)
        self.dispositionButton_1x3.setIconSize(QSize(40, 40))

        self.gridLayout_7.addWidget(self.dispositionButton_1x3, 0, 2, 1, 1)

        self.dispositionButton_1x2 = QPushButton(self.gridLayoutWidget_7)
        self.dispositionButton_1x2.setObjectName(u"dispositionButton_1x2")
        icon20 = QIcon()
        icon20.addFile(u"Assets/1x2grid.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.dispositionButton_1x2.setIcon(icon20)
        self.dispositionButton_1x2.setIconSize(QSize(40, 40))

        self.gridLayout_7.addWidget(self.dispositionButton_1x2, 0, 1, 1, 1)

        self.dispositionButton_1u2d = QPushButton(self.gridLayoutWidget_7)
        self.dispositionButton_1u2d.setObjectName(u"dispositionButton_1u2d")
        icon21 = QIcon()
        icon21.addFile(u"Assets/1up_2downgrid.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.dispositionButton_1u2d.setIcon(icon21)
        self.dispositionButton_1u2d.setIconSize(QSize(45, 45))

        self.gridLayout_7.addWidget(self.dispositionButton_1u2d, 1, 0, 1, 1)

        self.dispositionButton_1l2r = QPushButton(self.gridLayoutWidget_7)
        self.dispositionButton_1l2r.setObjectName(u"dispositionButton_1l2r")
        icon22 = QIcon()
        icon22.addFile(u"Assets/1+2grid.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.dispositionButton_1l2r.setIcon(icon22)
        self.dispositionButton_1l2r.setIconSize(QSize(45, 45))

        self.gridLayout_7.addWidget(self.dispositionButton_1l2r, 1, 2, 1, 1)

        self.label_14 = QLabel(self.frame_22)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(40, 0, 171, 31))
        self.label_14.setStyleSheet(u"font: 87 16pt \"Roboto\" \"bold\";\n"
"background-color: rgb(119, 118, 179);\n"
"color:#FFFFFF;\n"
"border-radius: 15px;")
        self.label_14.setTextFormat(Qt.PlainText)
        self.label_14.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.frame_22)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout_5.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.pantallaVisualizacion)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_5.addWidget(self.frame_3)

        self.stackedWidget.addWidget(self.pantallaVisualizacion)
        self.pantallaBaseDeDatos = QWidget()
        self.pantallaBaseDeDatos.setObjectName(u"pantallaBaseDeDatos")
        self.pantallaBaseDeDatos.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.stackedWidget.addWidget(self.pantallaBaseDeDatos)
        self.pantallaAnadirArchivo = QWidget()
        self.pantallaAnadirArchivo.setObjectName(u"pantallaAnadirArchivo")
        self.pantallaAnadirArchivo.setStyleSheet(u"\n"
"background-color: rgb(255, 255, 255);")
        self.horizontalLayout_2 = QHBoxLayout(self.pantallaAnadirArchivo)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalSpacer_5 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_5.addItem(self.verticalSpacer_5)

        self.label = QLabel(self.pantallaAnadirArchivo)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 50))
        palette = QPalette()
        brush = QBrush(QColor(90, 99, 156, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(255, 255, 255, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        self.label.setPalette(palette)
        font = QFont()
        font.setFamilies([u"Roboto"])
        font.setPointSize(24)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet(u"color:#5A639C")
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label)

        self.verticalSpacer_3 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_5.addItem(self.verticalSpacer_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.frame_24 = QFrame(self.pantallaAnadirArchivo)
        self.frame_24.setObjectName(u"frame_24")
        self.frame_24.setMinimumSize(QSize(0, 400))
        self.frame_24.setMaximumSize(QSize(16777215, 2000))
        self.frame_24.setStyleSheet(u"background-color: #E8C9ED;\n"
"border-radius: 15px;")
        self.frame_24.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_7 = QVBoxLayout(self.frame_24)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.frame_25 = QFrame(self.frame_24)
        self.frame_25.setObjectName(u"frame_25")
        self.frame_25.setMinimumSize(QSize(10, 0))
        self.frame_25.setMaximumSize(QSize(16777215, 1000))
        self.frame_25.setStyleSheet(u"border: 2px dashed #5A639C;\n"
"border-radius: 15px;")
        self.frame_25.setFrameShape(QFrame.NoFrame)
        self.gridLayout_2 = QGridLayout(self.frame_25)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.verticalSpacer_6, 0, 0, 1, 1)

        self.pushButton = QPushButton(self.frame_25)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"border: 2px dashed #E8C9ED;")
        icon23 = QIcon()
        icon23.addFile(u":/icons/Assets/icon_documentUpload.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton.setIcon(icon23)
        self.pushButton.setIconSize(QSize(160, 160))

        self.gridLayout_2.addWidget(self.pushButton, 1, 0, 1, 1)

        self.label_2 = QLabel(self.frame_25)
        self.label_2.setObjectName(u"label_2")
        font1 = QFont()
        font1.setFamilies([u"Roboto"])
        font1.setBold(True)
        self.label_2.setFont(font1)
        self.label_2.setStyleSheet(u"border: 2px dashed #E8C9ED;")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.verticalSpacer_7, 3, 0, 1, 1)


        self.verticalLayout_7.addWidget(self.frame_25)


        self.horizontalLayout_3.addWidget(self.frame_24)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.verticalSpacer_4 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout_5.addItem(self.verticalSpacer_4)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer = QSpacerItem(10, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.archivoButton_carpeta = QPushButton(self.pantallaAnadirArchivo)
        self.archivoButton_carpeta.setObjectName(u"archivoButton_carpeta")
        self.archivoButton_carpeta.setMinimumSize(QSize(200, 50))
        font2 = QFont()
        font2.setFamilies([u"Roboto"])
        font2.setPointSize(12)
        font2.setBold(True)
        self.archivoButton_carpeta.setFont(font2)
        self.archivoButton_carpeta.setStyleSheet(u"background-color: rgb(90, 99, 156);\n"
"color:#ffffff;\n"
"border-radius:15px;")

        self.horizontalLayout_4.addWidget(self.archivoButton_carpeta)

        self.horizontalSpacer_2 = QSpacerItem(10, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.archivoButton_carpeta_2 = QPushButton(self.pantallaAnadirArchivo)
        self.archivoButton_carpeta_2.setObjectName(u"archivoButton_carpeta_2")
        self.archivoButton_carpeta_2.setMinimumSize(QSize(200, 50))
        self.archivoButton_carpeta_2.setFont(font2)
        self.archivoButton_carpeta_2.setStyleSheet(u"background-color: rgb(90, 99, 156);\n"
"color:#ffffff;\n"
"border-radius:15px;")

        self.horizontalLayout_4.addWidget(self.archivoButton_carpeta_2)

        self.horizontalSpacer_3 = QSpacerItem(10, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)


        self.verticalLayout_5.addLayout(self.horizontalLayout_4)


        self.horizontalLayout_2.addLayout(self.verticalLayout_5)

        self.stackedWidget.addWidget(self.pantallaAnadirArchivo)

        self.horizontalLayout.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.mainButton_DB.setText("")
        self.mainButton_visualizacion.setText("")
        self.mainButton_anadirArchivo.setText("")
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Herramientas", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Funciones", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Disposici\u00f3n", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Carga de Archivos", None))
        self.pushButton.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:20pt; color:#5a639c;\">Arrastre y suelte los archivos </span></p><p><span style=\" font-size:20pt; color:#5a639c;\">DICOM ac\u00e1</span></p></body></html>", None))
        self.archivoButton_carpeta.setText(QCoreApplication.translate("MainWindow", u"Seleccionar carpeta", None))
        self.archivoButton_carpeta_2.setText(QCoreApplication.translate("MainWindow", u"Seleccionar archivo", None))
    # retranslateUi

