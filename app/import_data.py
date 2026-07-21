import pandas as pd
from sqlalchemy import create_engine

print("Starting import...")

engine = create_engine("sqlite:///data/ecochem.db")

df = pd.read_csv("data/ingredient_database_1000.csv")

print(df.head())

df.to_sql("ingredients", engine, if_exists="append", index=False)

print(f"Imported {len(df)} rows!")
