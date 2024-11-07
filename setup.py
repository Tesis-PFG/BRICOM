from cx_Freeze import setup, Executable

# Configuración de opciones de compilación
build_options = {
    'packages': ['pydicom', 'vtk', 'gdcm'],  # Incluye 'gdcm' y otros módulos necesarios
    'includes': ['pydicom.pixel_data_handlers.gdcm_handler'],
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
