Comandos:
- git clone <link>
- (iniciar la aplicación de qt y abrir el archivo .ui)
- *Comando para convertir el archivo .ui a .py:*
- Correr el main


Comandos Generación Código:
- pyuic5 -x .\ventana1.ui -o generatedInterface.py  #Genera la interfaz en python (autogenerado)
- pyuic5 -x .\dialog.ui -o generatedDialog.py  #Genera el diálogo de verificación de archivo en python (autogenerado)
- pyrcc5 -o .\resources_rc.py .\resources.qrc #Genera los recursos
- python main.py #Corre la interfaz con la lógica integrada