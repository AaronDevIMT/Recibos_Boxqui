from datos import cargar_datos_localidad, limpiar_datos
from generador import (
    cargar_elementos_visuales,
    crear_base_recibo,
    dibujar_recibo,
    guardar_recibo,
    generar_lista_cobro_excel,
    generar_id_recibo
)
from helpers import crear_carpeta_salida, obtener_fecha_corte
import pandas as pd

def main():
    # Selección de localidad
    localidad_id = input("Selecciona la sección a generar:\n 1. LOCALIDAD 1  2. LOCALIDAD 2  3. LOCALIDAD 3 4. LOCALIDAD 4 5. LOCALIDAD 5\n")

    # Cargar datos
    excel_path = "data/Cuadro de pagos.xlsx"
    data, saldo, nombre_localidad = cargar_datos_localidad(localidad_id, excel_path)
    data_seguro = pd.read_excel(excel_path, sheet_name="CLIENTES CON SEGURO", header=1)

    # Limpiar
    data, saldo, data_num = limpiar_datos(data, saldo, data_seguro)

    # Fechas y carpeta
    mes_str, anio_str, fecha_corte_str = obtener_fecha_corte()
    output_folder = crear_carpeta_salida(f"{anio_str}-{mes_str}", nombre_localidad)

    # Recursos visuales
    logo, icono, fuentes = cargar_elementos_visuales()

    # 🖨 Recibos
    no_recibos = []
    for _, row in data.iterrows():
        recibo, draw = crear_base_recibo()
        id_recibo = generar_id_recibo(row["NO"], mes_str, anio_str, nombre_localidad)
        dibujar_recibo(draw, recibo, fuentes, row, nombre_localidad, id_recibo, fecha_corte_str, logo, icono)
        guardar_recibo(recibo, f"{output_folder}/recibo_{row['NO']}.jpg")
        no_recibos.append(id_recibo)

    # 📄 Lista cobro
    generar_lista_cobro_excel(data, no_recibos, nombre_localidad, f"{output_folder}/lista_cobro_{nombre_localidad}.xlsx")

    print(f"✅ Recibos y lista de cobro generados en: {output_folder}")

if __name__ == "__main__":
    main()
