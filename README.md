Comandos:
- git clone <link>
- (iniciar la aplicación de qt y abrir el archivo .ui)
- *Comando para convertir el archivo .ui a .py:*
- Correr el main


Comandos Generación Código:
- pyside6-uic .\ventana1.ui > generatedApp.py  #Genera la interfaz
    ->Importante modificar el UTF generado de 16 a 8
    -> Cambiar import resources_rc (linea 21) por 
- pyside6-rcc .\resources.qrc -o .\resources_rc.py  #Genera los recursos