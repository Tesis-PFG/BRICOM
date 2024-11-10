
## Direcciones al ejecutable

QT-INT > build > exe.win-amd64-3.12 > main.exe

Comandos:

## Nuevo comando para correr el codigo
```
python -m controller.main
```

--

## código para generar ejecutable (estar en carpeta raíz)
```
python setup.py build
```

--

nota: es importante tener instalado cx-Freeze (ya agregado a requirements)

# Trabajo con el código:

```
git clone <link>
```
- Correr el main

### Comandos para la creación y activación del ambiente virtual:
```
python -m venv env
```

```
.\env\Scripts\activate
```

### Comandos para descarga de requerimientos:

```
pip install -r requirements.txt
```


### Comandos Generación Código:

```
pyuic5 -x .\ventanaPrincipal.ui -o generatedInterface.py  #Genera la interfaz en python (autogenerado)
```

```
pyuic5 -x .\dialogoTagsSubida.ui -o generatedDialogTagsSubida.py  #Genera el diálogo de verificación de archivo en python (autogenerado)
```

```
pyuic5 -x .\dialog_escoger_estudio.ui -o generatedDialogEscogerEstudio.py
```

```
pyuic5 -x .\dialog_inicio.ui -o generatedDialogInicio.py
```

```
pyuic5 -x .\dialog_carga.ui -o generatedDialogCarga.py
```

```
python -m controller.main #Corre la interfaz con la lógica integrada
```