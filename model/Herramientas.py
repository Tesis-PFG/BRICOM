from PyQt5 import QtWidgets, QtCore,QtGui
from app.interface.OrthoViewer import *
from app.interface.Worker import *
from app.interface.QtViewer import *
import math

class AngleMeasurement(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

        # Configurar el tamaño del canvas
        self.setFixedSize(parent.size())

        # Habilitar fondo transparente
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)

        # Crear un QPixmap transparente para dibujar
        self.pixmap = QtGui.QPixmap(self.size())
        self.pixmap.fill(QtCore.Qt.transparent)  # Fondo transparente
        self.setPixmap(self.pixmap)

        # Variables para almacenar los puntos
        self.point1 = None  # Punto x1
        self.point2 = None  # Punto x2
        self.point3 = None  # Punto y

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(0, 0, self.pixmap)

        # Dibujar las líneas y el ángulo calculado si los tres puntos están definidos
        if self.point1 and self.point2 and self.point3:
            painter.setPen(QtGui.QPen(Qt.blue, 2))
            # Línea base (x1 -> x2)
            painter.drawLine(self.point1, self.point2)
            # Línea de medición (x2 -> y)
            painter.drawLine(self.point2, self.point3)

            # Calcular el ángulo y dibujarlo cerca del tercer punto
            angle = self.calculate_angle()
            painter.setPen(QtGui.QPen(Qt.white))
            painter.drawText(self.point3, f"Ángulo: {angle:.2f}°")

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if not self.point1:
                # Primer clic, establece el punto x1
                self.point1 = event.pos()
            elif not self.point2:
                # Segundo clic, establece el punto x2 (base)
                self.point2 = event.pos()
            elif not self.point3:
                # Tercer clic, establece el punto y y realiza el cálculo del ángulo
                self.point3 = event.pos()
                self.update()  # Redibujar para mostrar el ángulo
            else:
                # Si ya se tienen los tres puntos, reiniciar la medición
                self.clear_canvas()
                self.point1 = event.pos()  # Empezar con el nuevo primer punto

    def calculate_angle(self):
        """Calcula el ángulo en el rango [0°, 180°] entre la línea x1->x2 y la línea x2->y."""
        # Vectores de las dos líneas
        dx1 = self.point2.x() - self.point1.x()
        dy1 = self.point2.y() - self.point1.y()
        dx2 = self.point3.x() - self.point2.x()
        dy2 = self.point3.y() - self.point2.y()

        # Producto punto de los vectores
        dot_product = dx1 * dx2 + dy1 * dy2
        # Magnitud de los vectores
        mag1 = math.sqrt(dx1**2 + dy1**2)
        mag2 = math.sqrt(dx2**2 + dy2**2)

        # Evitar divisiones por cero
        if mag1 == 0 or mag2 == 0:
            return 0.0

        # Calcular el ángulo en radianes y convertirlo a grados
        angle_rad = math.acos(dot_product / (mag1 * mag2))
        angle_deg = math.degrees(angle_rad)

        # Determinar el sentido del ángulo usando el producto cruzado
        cross_product = dx1 * dy2 - dy1 * dx2
        if cross_product < 0:
            # Si el producto cruzado es negativo, ajustar el ángulo a su complemento
            angle_deg = 360 - angle_deg

        # Asegurar que el ángulo esté entre 0 y 180 grados
        if angle_deg > 180:
            angle_deg = 360 - angle_deg

        return angle_deg

    def clear_canvas(self):
        """Limpia los puntos y el ángulo del canvas para una nueva medición."""
        self.point1 = None
        self.point2 = None
        self.point3 = None
        self.pixmap.fill(QtCore.Qt.transparent)  # Limpiar el pixmap
        self.update()  # Redibujar el canvas


class TextCanvas(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

        # Configurar el tamaño del canvas
        self.setFixedSize(parent.size())

        # Habilitar el fondo transparente
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)

        # Crear un QPixmap transparente para dibujar
        self.pixmap = QtGui.QPixmap(self.size())
        self.pixmap.fill(QtCore.Qt.transparent)  # Fondo transparente
        self.setPixmap(self.pixmap)

        # Variables para almacenar el estado del texto
        self.current_text = ""  # Texto que se está escribiendo
        self.text_position = None  # Posición donde se colocará el texto

    def paintEvent(self, event):
        # Crear un painter para el widget actual
        painter = QtGui.QPainter(self)

        # Dibujar el contenido del pixmap actual en el widget
        painter.drawPixmap(0, 0, self.pixmap)

        # Dibujar el texto temporalmente mientras se escribe
        if self.text_position is not None:
            painter.setPen(QtGui.QPen(Qt.white))  # Color del texto
            painter.drawText(self.text_position, self.current_text)  # Dibuja el texto en la posición
        painter.end()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            # Captura la posición del clic para el texto
            self.text_position = QtCore.QPoint(event.x(), event.y())
            self.current_text = ""  # Reiniciar el texto actual
            self.setFocus()  # Asegurarse de que el canvas tenga el foco para capturar teclas

    def keyPressEvent(self, event):
        if self.text_position is not None:
            # Captura las teclas pulsadas y añade texto
            if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
                # Cuando se presiona Enter, dibujar el texto de forma permanente en el pixmap
                self.commit_text()
            elif event.key() == QtCore.Qt.Key_Backspace:
                # Borrar el último carácter
                self.current_text = self.current_text[:-1]
            else:
                # Agregar el carácter al texto actual
                self.current_text += event.text()

            # Actualizar el canvas para mostrar el texto mientras se escribe
            self.update()

    def commit_text(self):
        """Dibuja el texto de forma permanente en el QPixmap cuando se presiona Enter."""
        if self.text_position is not None and self.current_text:
            # Crear un painter para dibujar permanentemente en el QPixmap
            painter = QtGui.QPainter(self.pixmap)
            painter.setPen(QtGui.QPen(Qt.black))  # Color del texto
            painter.drawText(self.text_position, self.current_text)  # Dibuja el texto en la posición
            painter.end()

            # Finaliza la entrada de texto
            self.text_position = None  # Limpiar la posición del texto
            self.update()  # Redibujar el canvas para mostrar el estado actualizado

    def clear_canvas(self):
        """Limpia el canvas y borra todo el contenido."""
        self.pixmap.fill(QtCore.Qt.transparent)  # Limpiar el pixmap
        self.current_text = ""  # Limpiar el texto actual
        self.text_position = None  # Limpiar la posición del texto
        self.update()  # Redibujar el canvas para mostrar el estado limpio


class ShapeCanvas(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

        # Configurar el tamaño del canvas
        self.setFixedSize(parent.size())

        # Habilitar el fondo transparente y evitar que el canvas bloquee la imagen subyacente
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

        # Crear un QPixmap transparente para dibujar
        self.pixmap = QtGui.QPixmap(self.size())
        self.pixmap.fill(QtCore.Qt.transparent)  # Fondo transparente
        self.setPixmap(self.pixmap)

        self.start_x = None
        self.start_y = None
        self.current_shape = None  # Para almacenar el tipo de forma a dibujar

    def paintEvent(self, event):
        # Dibujar el contenido del pixmap actual
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.drawPixmap(0, 0, self.pixmap)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if self.start_x is None and self.start_y is None:
                # Primer clic: almacenar la posición inicial
                self.start_x = event.x()
                self.start_y = event.y()
                self.update()
            else:
                # Segundo clic: dibujar la figura
                end_x = event.x()
                end_y = event.y()
                self.draw_shape(end_x, end_y)  # Dibuja la figura con el segundo clic
                self.start_x = None  # Reiniciar las coordenadas
                self.start_y = None
                self.update()

    def draw_shape(self, end_x, end_y):
        # Crear un nuevo painter para dibujar la figura
        painter = QtGui.QPainter(self.pixmap)

        if self.current_shape == "circle":
            radius = int(math.hypot(end_x - self.start_x, end_y - self.start_y))  # Distancia
            painter.setPen(QtGui.QPen(Qt.blue, 2))  # Color y grosor del borde
            painter.setBrush(QtGui.QBrush(Qt.transparent))  # Relleno transparente
            painter.drawEllipse(self.start_x - radius, self.start_y - radius, 2 * radius, 2 * radius)

        elif self.current_shape == "square":
            size = max(abs(end_x - self.start_x), abs(end_y - self.start_y))  # Tamaño dinámico
            painter.setPen(QtGui.QPen(Qt.red, 2))  # Color y grosor del borde
            painter.setBrush(QtGui.QBrush(Qt.transparent))  # Relleno transparente
            painter.drawRect(self.start_x, self.start_y, size, size)
        elif self.current_shape == "arrow":
            # Dibujar la línea de la flecha
            painter.setPen(QtGui.QPen(Qt.green, 2))  # Color y grosor del borde
            painter.drawLine(self.start_x, self.start_y, end_x, end_y)  # Línea principal
            self.draw_arrow_head(painter, end_x, end_y)  # Dibujar la cabeza de la flecha

        painter.end()

        # Actualizar el widget para mostrar el nuevo dibujo
        self.update()  # Redibujar el canvas

    def draw_arrow_head(self, painter, end_x, end_y):
        """Dibuja la cabeza de la flecha en el extremo de la línea."""
        arrow_size = 10  # Tamaño de la cabeza de la flecha

        # Calcular los ángulos de la línea
        angle = math.atan2(end_y - self.start_y, end_x - self.start_x)

        # Puntos para las puntas de la flecha
        point1_x = end_x - arrow_size * math.cos(angle - math.pi / 6)
        point1_y = end_y - arrow_size * math.sin(angle - math.pi / 6)

        point2_x = end_x - arrow_size * math.cos(angle + math.pi / 6)
        point2_y = end_y - arrow_size * math.sin(angle + math.pi / 6)

        # Dibujar las puntas de la flecha
        painter.setBrush(QtGui.QBrush(Qt.green))  # Color de la cabeza de la flecha
        painter.drawPolygon(QtGui.QPolygon([QtCore.QPoint(int(end_x), int(end_y)),
                                           QtCore.QPoint(int(point1_x), int(point1_y)),
                                           QtCore.QPoint(int(point2_x), int(point2_y))]))

    def clear_canvas(self):
        print("Borrando el canvas...")  # Mensaje de depuración
        self.pixmap.fill(QtCore.Qt.transparent)  # Limpiar el pixmap
        self.update()  # Redibujar el canvas para mostrar el estado limpio
        print("Canvas borrado.")  # Mensaje de depuración

    def set_shape(self, shape):
        """Método para establecer la forma a dibujar ('circle' o 'square')."""
        if shape in ["circle", "square", "arrow"]:
            self.current_shape = shape
        else:
            raise ValueError("Forma no válida. Usa 'circle' o 'square'.")

class Canvas(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

        # Configurar el tamaño del canvas
        self.setFixedSize(parent.size())

        # Habilitar el fondo transparente y evitar que el canvas bloquee la imagen subyacente
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

        # Crear un QPixmap transparente para dibujar
        self.pixmap = QtGui.QPixmap(self.size())
        self.pixmap.fill(QtCore.Qt.transparent)
        self.setPixmap(self.pixmap)

        self.last_x, self.last_y = None, None
        self.pen_color = QtGui.QColor('#ff0000')

    def paintEvent(self, event):
        # Dibujar el contenido del pixmap actual sin redibujar el fondo
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.drawPixmap(0, 0, self.pixmap)

    def mouseMoveEvent(self, e):
        if self.last_x is None:
            self.last_x = e.x()
            self.last_y = e.y()
            return

        if e.buttons() == QtCore.Qt.LeftButton:
            painter = QtGui.QPainter(self.pixmap)
            pen = QtGui.QPen(self.pen_color, 4, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
            painter.setPen(pen)
            painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
            painter.end()
            self.update()

        self.last_x = e.x()
        self.last_y = e.y()

    def mousePressEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.last_x = e.x()
            self.last_y = e.y()
            self.update()

    def mouseReleaseEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.last_x = None
            self.last_y = None

    def clear_canvas(self):
        self.pixmap.fill(QtCore.Qt.transparent)
        self.setPixmap(self.pixmap)
        self.update()

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
        if event.button() == QtCore.Qt.LeftButton:
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
        painter = QPainter(self)
        
        # Aquí nos aseguramos de no borrar la imagen de fondo
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
    
class DistanceMeasurementDicom(QWidget):
    def __init__(self, pixel_distance, parent=None):
        super().__init__(parent)
        self.start_point = None
        self.end_point = None
        self.is_measuring = False
        self.pixel_spacing = pixel_distance  # Extrae el tamaño de los píxeles
        
        # Set size of the canvas
        self.setFixedSize(parent.size())
        
        # Enable transparent background for the widget itself
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
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
        painter = QPainter(self)
        
        # No borramos el fondo, solo dibujamos sobre él
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

