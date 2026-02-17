#!/usr/bin/env python
# coding: utf-8

from pathlib import Path
DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
data_pt_path = DATA_DIR / 'data_prueba_técnica.csv'
data_pt_extracted_path = DATA_DIR / 'data_prueba_tecnica_extracted.csv'
data_pt_transformed_path = DATA_DIR / 'data_prueba_tecnica_transformed.csv'

# # Procesamiento y transferencia de datos
# 

# ## 1.1 Extracción de los datos
# Cargamos los datos desde el archivo. Insepeccionamos en busca de anomalías



import pandas as pd
import numpy as np

data_pt = pd.read_csv(data_pt_path)
data_pt.head()

data_pt.info()

# Vemos que existen 10000 entradas, pero existen entradas 
# con el campo id y company_id con valor nulo. Necesitamos saber 
# cuántos registros son y decidir cómo proceder.

missing_data = data_pt.isnull().sum()
missing_data

data_pt[data_pt['company_id'].isnull()]

data_pt[data_pt['id'].isnull()]

cells_num = np.prod(data_pt.shape)
missing_cells_num = missing_data.sum()
missing_data_percentage = (missing_cells_num / cells_num) * 100
print(f'Porcentaje de valores nulos en columna alguna columna: {round(missing_data_percentage, 2)}%')

# En estos casos es necesario preguntarse por los objetivos de los datos,
# o posibles anomalías en el proceso de recolección. Para tomar la 
# decisión se debe consultar con el equipo de trabajo.

# Como el porcentaje de datos nulos es muy bajo para esta prueba simplemente excluiremos estos datos.


data_pt = data_pt.dropna(subset=['id', 'company_id'])
data_pt.info()

data_pt.describe()

# Detectamos otra anomalía. La media y el máximo son infinitos. Este valor no está considerado dentro de nuestro esquema. Es necesario detectar cuántos registros están involucrados y decidir.


inf_values_num = np.isinf(data_pt['amount']).sum()
print(f'Existe(n) {int(inf_values_num)} valores infinitos')
data_pt[np.isinf(data_pt['amount'])]

# Reemplazamos los valores infinitos con NaN para observar cómo cambia el describe


data_pt = data_pt.replace([np.inf, -np.inf], np.nan, inplace=True)
data_pt.describe()

# Observamos que el valor máximo de la columna 'amount' tiene 34 cifras. El esquema requerido tiene un valor máximo de 16 cifras. Es necesario identificar a los valores que no cumplen con esta característica.


too_big_amount = data_pt[data_pt['amount'] > 9_999_999_999_999_999].shape[0]
print(f'Existen {too_big_amount} registros con amount demasiado grande')

# Como son pocos valores, en esta prueba, simplemente los excluímos.


data_pt = data_pt[data_pt['amount'] <= 9_999_999_999_999_999]
data_pt.info()

# Guardamos la información extraída de vuelta en formato CSV.


data_pt.to_csv(data_pt_extracted_path, index=False)

# # 1.2 Transformación de los datos
# Pasamos al proceso de ajustar el formato de los datos al requerimiento del esquema


import pandas as pd
# Cargar archivo
df = pd.read_csv(data_pt_extracted_path)

# Renombrar columnas
df = df.rename(columns={
    "name": "company_name"
})

# Conversión de tipos
df["id"] = df["id"].astype(str)
df["company_id"] = df["company_id"].astype(str)

df["amount"] = df["amount"].astype(float).round(2)

df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
df["paid_at"] = pd.to_datetime(df["paid_at"], errors="coerce")

# Limitar longitudes
df["id"] = df["id"].str.slice(0, 24)
df["company_id"] = df["company_id"].str.slice(0, 24)
df["company_name"] = df["company_name"].str.slice(0, 130)
df["status"] = df["status"].str.slice(0, 30)
# Reordenar columnas según el esquema
df = df[
    [
        "id",
        "company_name",
        "company_id",
        "amount",
        "status",
        "created_at",
        "paid_at",
    ]
]
df.head()


# Ejecutamos validaciones para comprobar que se cumplen los requerimientos

# IDs no nulos
assert df["id"].notna().all()
assert df["company_id"].notna().all()

# Amount válido
assert (df["amount"] >= 0).all()
assert (df["amount"] <= 9_999_999_999_999_999).all()

# # 1.3 Carga de los datos
# En este proceso registramos los datos transformados de forma persistente en la base de datos

from sqlalchemy import create_engine
# Conexión MySQL
engine = create_engine(
    "mysql+mysqlconnector://appuser:apppass@localhost:8080/transacciones_db"
)

# Insertar datos
df.to_sql(
    name="cargo",
    con=engine,
    if_exists="append",
    index=False,
)

# El número resultado nos indica el número de columnas afectadas. Podemos comprobarlo directamente con una consulta SQL.

# Ejecutar consulta
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM cargo;"))
    total = result.scalar()

print(f"Total de registros en Cargo: {total}")

# Guardamos la información también en formato CSV para seguir procesándo en la etapa de normalización.

df.to_csv(data_pt_transformed_path, index=False)
