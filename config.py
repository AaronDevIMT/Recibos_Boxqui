import os
import sys

# Detectar la ruta base dependiendo del contexto
if getattr(sys, 'frozen', False):
    # Si es ejecutado como .exe
    BASE_DIR = sys._MEIPASS
    RUTA_EJECUCION = os.path.dirname(sys.executable)  # para guardar archivos
else:
    # Si es ejecutado como script .py
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    RUTA_EJECUCION = BASE_DIR

# Rutas de imágenes
RUTA_LOGO = os.path.join(BASE_DIR, "assets", "logo.png")
# Logo pequeño (FrameInicio)
RUTA_LOGO_SMALL = os.path.join(BASE_DIR, "assets", "logo.ico")

RUTA_ICONO = os.path.join(BASE_DIR, "assets", "icono.png")

# Rutas de fuentes
FONT_PATH_BOLD = os.path.join(BASE_DIR, "arialbd.ttf")
FONT_PATH_REGULAR = os.path.join(BASE_DIR, "arial.ttf")
FONT_PATH_SMALL = os.path.join(BASE_DIR, "arial.ttf")

# Diccionario de meses
MESES_ES = {
    "01": "ENERO", "02": "FEBRERO", "03": "MARZO", "04": "ABRIL",
    "05": "MAYO", "06": "JUNIO", "07": "JULIO", "08": "AGOSTO",
    "09": "SEPTIEMBRE", "10": "OCTUBRE", "11": "NOVIEMBRE", "12": "DICIEMBRE"
}