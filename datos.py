import pandas as pd

def limpiar_datos(data: pd.DataFrame, saldo: pd.DataFrame, data_seguro: pd.DataFrame):
    """
    Limpia los datos de clientes y prepara la información numérica.
    - Elimina filas vacías
    - Filtra clientes activos (estado = 'A')
    - Limpia nombres
    - Convierte a tipos correctos
    - Suma montos de seguro si aplica
    """
    columnas_meses = [
        'ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO',
        'JULIO', 'AGOSTO', 'SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE', 'ADEUDO AÑO ANTERIOR'
    ]

    # Eliminar filas sin nombre
    data['NOMBRE DEL CLIENTE'] = data['NOMBRE DEL CLIENTE'].astype(str).str.strip()
    data = data[data['NOMBRE DEL CLIENTE'].notna() & (data['NOMBRE DEL CLIENTE'] != '')]

    # Filtrar solo clientes activos
    data = data[data['ESTADO'] == 'A']
    

    # Normalizar nombres de data_seguro
    data_seguro['NOMBRE DEL CLIENTE'] = data_seguro['NOMBRE DEL CLIENTE'].astype(str).str.replace(r'\s*\(.*?\)', '', regex=True)

    data = data[data['NO'].notna()]
    saldo = saldo[saldo['NO'].notna()]

    data['NO'] = data['NO'].astype(int)
    saldo.loc[:, 'NO'] = saldo['NO'].astype(int)


    data = data.fillna(0).infer_objects(copy=False)
    data_num = data[columnas_meses].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)
    data_seguro_num = data_seguro[columnas_meses].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

    # Sumar seguro si aplica
    for i, row in data.iterrows():
        nombre = row['NOMBRE DEL CLIENTE']
        if nombre in data_seguro['NOMBRE DEL CLIENTE'].values:
            index_seguro = data_seguro[data_seguro['NOMBRE DEL CLIENTE'] == nombre].index[0]
            data_num.loc[i] += data_seguro_num.loc[index_seguro]

    data['Suma'] = data_num.sum(axis=1)

    # Guardar una copia del nombre original para lista de cobro
    data['NOMBRE_DEL_CLIENTE_REF'] = data['NOMBRE DEL CLIENTE']

    # Limpiar nombre solo para el recibo
    data['NOMBRE DEL CLIENTE'] = data['NOMBRE DEL CLIENTE'].astype(str).str.replace(r'\s*\(.*?\)', '', regex=True)
    data_seguro['NOMBRE DEL CLIENTE'] = data_seguro['NOMBRE DEL CLIENTE'].astype(str).str.replace(r'\s*\(.*?\)', '', regex=True)


    return data, saldo, data_num


def cargar_datos_localidad(localidad_id: str, excel_path: str):
    """Carga los datos de la hoja Excel correspondiente a la localidad."""
    # ⚠️ Mapeo censurado para demo
    # Este mapeo conecta ID de localidad con nombres de hojas y títulos
    # En la versión pública, se muestran ejemplos ficticios

    mapeo = {
        '1': ("HOJA_CLIENTES_LOC1", "LISTA_COBRO_LOC1", "Localidad 1"),
        '2': ("HOJA_CLIENTES_LOC2", "LISTA_COBRO_LOC2", "Localidad 2"),
        '3': ("HOJA_CLIENTES_LOC3", "LISTA_COBRO_LOC3", "Localidad 3"),
        '4': ("HOJA_CLIENTES_LOC4", "LISTA_COBRO_LOC4", "Localidad 4"),
        '5': ("HOJA_CLIENTES_LOC5", "LISTA_COBRO_LOC5", "Localidad 5")
    }

    if localidad_id not in mapeo:
        raise ValueError("ID de localidad inválido")

    hoja_clientes, hoja_saldo, nombre_localidad = mapeo[localidad_id]
    data = pd.read_excel(excel_path, sheet_name=hoja_clientes, header=1)
    saldo = pd.read_excel(excel_path, sheet_name=hoja_saldo, header=1)

    return data, saldo, nombre_localidad

# Diccionario: ID → nombre (versión demo)
LOCALIDADES_POR_ID = {
    '1': "Localidad 1",
    '2': "Localidad 2",
    '3': "Localidad 3",
    '4': "Localidad 4",
    '5': "Localidad 5"
}

# Diccionario inverso: nombre → ID (útil para búsqueda por nombre)
LOCALIDADES_NOMBRE_A_ID = {v: k for k, v in LOCALIDADES_POR_ID.items()}

def cargar_datos_localidad_por_nombre(nombre_localidad: str, excel_path: str):
    """Busca el ID correspondiente al nombre de localidad y carga los datos."""
    from datos import LOCALIDADES_NOMBRE_A_ID
    localidad_id = LOCALIDADES_NOMBRE_A_ID.get(nombre_localidad)
    if not localidad_id:
        raise ValueError(f"Nombre de localidad no reconocido: {nombre_localidad}")
    return cargar_datos_localidad(localidad_id, excel_path)
