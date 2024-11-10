from cx_Freeze import setup, Executable
import os

build_options = {
    'packages': ['pydicom', 'vtk', 'gdcm'], 
    'includes': ['pydicom.pixel_data_handlers.gdcm_handler'],
    'include_files': [
        ('Assets', 'Assets'),  
        ('app/assets', 'app/assets'),
        ('Data', 'Data'),
        ('temp', 'temp') 
    ]
}


base = 'Win32GUI'
setup(
    name="AppRegistro",
    version="0.1",
    description="Interfaz gráfica de registro de imágenes TAC y RM",
    options={'build_exe': build_options},
    executables=[Executable('controller/main.py', base=base, icon='Assets/BRICOM_logo.ico')],
)