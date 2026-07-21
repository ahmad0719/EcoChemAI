
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///data/ecochem.db")

with engine.connect() as conn:
	result = conn.execute(text("SELECT COUNT(*) FROM ingredients"))
	print("Total ingredients:", result.scalar())

	result = conn.execute(text("SELECT * FROM ingredients LIMIT 10"))
	for row in result:
		print(row)
