from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "ecochem.db"

print(f"Using database: {DB_PATH}")

engine = create_engine(f"sqlite:///{DB_PATH}")

def search_ingredient(name):
    query = """
    SELECT *
    FROM ingredients
    WHERE Ingredient LIKE ?
    LIMIT 5
    """

    return pd.read_sql(query, engine, params=(f"%{name}%",))
    
