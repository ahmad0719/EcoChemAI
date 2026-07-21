from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///data/ecochem.db")

print("=== EcoChemAI Ingredient Search ===")

while True:
    ingredient = input("\nSearch ingredient (or 'exit'): ")

    if ingredient.lower() == "exit":
        break

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT Ingredient, Function, Category
                FROM ingredients
                WHERE Ingredient LIKE :name
                LIMIT 10
            """),
            {"name": f"%{ingredient}%"}
        )

        rows = result.fetchall()

        if not rows:
            print("No ingredient found.")
        else:
            print("\nResults:\n")

            for row in rows:
                print(f"Ingredient : {row[0]}")
                print(f"Function   : {row[1]}")
                print(f"Category   : {row[2]}")
                print("-" * 40)
