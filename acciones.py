import os
import pandas as pd
from helpers import crear_carpeta_salida
from datos import cargar_datos_localidad, limpiar_datos, LOCALIDADES_NOMBRE_A_ID
from generador import (
    cargar_elementos_visuales,
    crear_base_recibo,
    dibujar_recibo,
    guardar_recibo,
    generar_lista_cobro_excel,
    generar_id_recibo
)

def generar_todos(localidad_nombre, excel_path, mes_str, anio_str, fecha_corte_str):
    """
    Genera recibos de todos los clientes de una localidad para un mes y año específicos.
    """
    loc_id = LOCALIDADES_NOMBRE_A_ID[localidad_nombre]

    # Cargar y limpiar datos
    data, saldo, nombre_localidad = cargar_datos_localidad(loc_id, excel_path)
    data_seguro = pd.read_excel(excel_path, sheet_name="CLIENTES CON SEGURO", header=1)
    data, saldo, _ = limpiar_datos(data, saldo, data_seguro)

    # Crear carpeta de salida
    output_folder = crear_carpeta_salida(f"{anio_str}-{mes_str}", nombre_localidad)
    logo, icono, fuentes = cargar_elementos_visuales()
    no_recibos = []

    # Generar recibos
    for _, row in data.iterrows():
        recibo, draw = crear_base_recibo()
        id_recibo = generar_id_recibo(row["NO"], mes_str, anio_str, nombre_localidad)
        dibujar_recibo(draw, recibo, fuentes, row, nombre_localidad, id_recibo, fecha_corte_str, logo, icono)
        guardar_recibo(recibo, os.path.join(output_folder, f"recibo_{row['NO']}.jpg"))
        no_recibos.append(id_recibo)

    # Generar lista de cobro
    generar_lista_cobro_excel(data, no_recibos, nombre_localidad,
                              os.path.join(output_folder, f"lista_cobro_{nombre_localidad}.xlsx"))
    return output_folder


def generar_individual(localidad_nombre, excel_path, mes_str, anio_str, fecha_corte_str, cliente_no):
    """
    Genera un recibo individual para un cliente específico.
    """
    loc_id = LOCALIDADES_NOMBRE_A_ID[localidad_nombre]

    # Cargar y limpiar datos
    data, saldo, nombre_localidad = cargar_datos_localidad(loc_id, excel_path)
    data_seguro = pd.read_excel(excel_path, sheet_name="CLIENTES CON SEGURO", header=1)
    data, saldo, _ = limpiar_datos(data, saldo, data_seguro)

    # Filtrar cliente
    cliente_data = data[data['NO'] == int(cliente_no)]
    if cliente_data.empty:
        raise ValueError("Cliente no encontrado.")

    # Crear carpeta de salida
    output_folder = crear_carpeta_salida(f"{anio_str}-{mes_str}", nombre_localidad)
    logo, icono, fuentes = cargar_elementos_visuales()

    # Generar recibo
    for _, row in cliente_data.iterrows():
        recibo, draw = crear_base_recibo()
        id_recibo = generar_id_recibo(row["NO"], mes_str, anio_str, nombre_localidad)
        dibujar_recibo(draw, recibo, fuentes, row, nombre_localidad, id_recibo, fecha_corte_str, logo, icono)
        guardar_recibo(recibo, os.path.join(output_folder, f"recibo_{row['NO']}.jpg"))

    return output_folder
 
 # Acciones