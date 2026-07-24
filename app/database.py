from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///data/ecochem.db"

engine = create_engine(DATABASE_URL)
