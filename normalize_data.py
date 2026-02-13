import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv('data_prueba_tecnica_transformed.csv')

companies_df = (
    df[["company_id", "company_name"]]
    .dropna(subset=["company_id"])
    .drop_duplicates()
)

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

engine = create_engine(
    "mysql+mysqlconnector://appuser:apppass@localhost:3306/payments_db"
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