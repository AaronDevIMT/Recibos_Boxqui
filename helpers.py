# helpers.py
import os
from datetime import datetime
from config import RUTA_EJECUCION

def crear_carpeta_salida(mes, localidad):
    """
    Crea la carpeta donde se guardarán los recibos.
    mes: string con formato YYYY-MM
    localidad: nombre de la localidad
    """
    output_folder = os.path.join(RUTA_EJECUCION, 'output', f"{mes}_{localidad}")
    os.makedirs(output_folder, exist_ok=True)
    return output_folder

def obtener_fecha_corte():
    """
    Devuelve:
    - mes_str (MM)
    - anio_str (YYYY)
    - fecha_corte_str (01-NOMBREMES-YYYY)
    """
    now = datetime.now()
    mes_str = f"{now.month:02d}"
    anio_str = str(now.year)
    return mes_str, anio_str
