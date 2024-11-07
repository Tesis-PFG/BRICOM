from cx_Freeze import setup, Executable
import os

# Configuración de opciones de compilación
build_options = {
    'packages': ['pydicom', 'vtk', 'gdcm'],  # Incluye 'gdcm' y otros módulos necesarios
    'includes': ['pydicom.pixel_data_handlers.gdcm_handler'],
    'include_files': [
        ('Assets', 'Assets'),  # Copia la carpeta Assets de la raíz
        ('app/assets', 'app/assets')  # Copia la carpeta assets dentro de app
    ]
}

# Definir el archivo principal
base = 'Win32GUI'  # Cambia a '' si es una aplicación sin consola
setup(
    name="TuAplicacion",
    version="0.1",
    description="Descripción de tu aplicación",
    options={'build_exe': build_options},
    executables=[Executable('controller/main.py', base=base)],
)
