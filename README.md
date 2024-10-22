Comandos:
- git clone <link>
- (iniciar la aplicación de qt y abrir el archivo .ui)
- *Comando para convertir el archivo .ui a .py:*
- Correr el main

Comandos para la creación y activación del ambiente virtual:
- python -m venv env
- .\env\Scripts\activate

Comandos para el descargue de requerimientos:
- pip install -r requirements.txt

Comandos Generación Código:
- pyuic5 -x .\ventanaPrincipal.ui -o generatedInterface.py  #Genera la interfaz en python (autogenerado)
- pyuic5 -x .\dialogoTagsSubida.ui -o generatedDialogTagsSubida.py  #Genera el diálogo de verificación de archivo en python (autogenerado)
- pyuic5 -x .\dialog_escoger_estudio.ui -o generatedDialogEscogerEstudio.py
- python main.py #Corre la interfaz con la lógica integrada