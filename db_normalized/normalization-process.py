#!/usr/bin/env python
# coding: utf-8

from pathlib import Path
DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
data_pt_transformed_path = DATA_DIR / 'data_prueba_tecnica_transformed.csv'

import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv(data_pt_transformed_path)


companies_df = (
    df[["company_id", "company_name"]]
    .dropna(subset=["company_id"])
    .drop_duplicates()
)
print("Número de compañías:", companies_df.shape[0])
companies_df

# Podemos observar que existe un duplicado para el campo 'company_id'. Existe un registro con valor en el campo 'company_name' nulo, y el otro sí tiene valor. Además de que aparecen variantes del mismo nombre, incluso una con el id no válido.
# 
# De manera juiciosa, eliminamos el registro con 'company_name' incorrectos, pues se corresponden con el otro registro que sí tiene valor en ese campo.
# 
# Este procedimiento manual es posible gracias a que son pocos registros para esta tabla. En general, es necesaria más información sobre la naturaleza y el propósito de los datos para ejecutar procedimientos más generales.

companies_df = companies_df[
    ~(
        (companies_df["company_id"] == "cbf1c8b09cd5b549416d49d2") &
        (
            companies_df["company_name"].isna() |
            (companies_df["company_name"] != "MiPasajefy")
        )
    )
]
companies_df


companies_df.shape

charges_df = df[
    [
        "id",
        "company_id",
        "amount",
        "status",
        "created_at",
        "paid_at",
    ]
]
charges_df.head()


engine = create_engine(
    "mysql+mysqlconnector://appuser:apppass@localhost:8081/transacciones_db"
)

companies_df.to_sql(
    name="companies",
    con=engine,
    if_exists="append",
    index=False
)

charges_df.to_sql(
    name="charges",
    con=engine,
    if_exists="append",
    index=False
)

# El número resultado nos indica el número de columnas afectadas. Podemos comprobarlo directamente con una consulta SQL.


# Ejecutar consulta
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM companies, charges;"))
    total = result.scalar()

print(f"Total de registros en Cargo: {total}")
