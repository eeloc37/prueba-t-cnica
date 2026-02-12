import pandas as pd
from sqlalchemy import create_engine

# Cargar archivo
df = pd.read_csv('prueba-técnica/data_prueba_tecnica_extracted.csv')

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
print(df.head())
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


# IDs no nulos
assert df["id"].notna().all()
assert df["company_id"].notna().all()

# Amount válido
assert (df["amount"] >= 0).all()
assert (df["amount"] <= 9_999_999_999_999_999).all()

# Conexión MySQL
engine = create_engine(
    "mysql+mysqlconnector://appuser:apppass@localhost:3306/transacciones_db"
)

# Insertar datos
df.to_sql(
    name="cargo",
    con=engine,
    if_exists="append",
    index=False,
)
# Guardar datos transformados en un nuevo CSV
df.to_csv("data_prueba_tecnica_transformed.csv", index=False)