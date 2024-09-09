from PySide6.QtWidgets import QApplication
from aplication import MyApp
import sys

app =QApplication(sys.argv)

window = MyApp()

window.show()
app.exec()