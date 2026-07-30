from pathlib import Path
import pandas as pd
import json

# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# Input: your enriched database
input_file = DATA_DIR / "ingredient_database_enriched.csv"

# Output: RAG knowledge documents
output_file = DATA_DIR / "rag_documents.json"

# Load database
df = pd.read_csv(input_file)

documents = []

# Fields we want to include when they contain data
fields = [
    "Function",
    "Category",
    "PubChem CID",
    "IUPAC Name",
    "Molecular Formula",
    "Molecular Weight",
]

for _, row in df.iterrows():

    ingredient = str(row["Ingredient"]).strip()

    # Skip empty ingredient names
    if not ingredient or ingredient.lower() == "nan":
        continue

    text_parts = [f"Ingredient: {ingredient}"]

    for field in fields:
        value = row.get(field)

        if pd.notna(value) and str(value).strip():
            text_parts.append(f"{field}: {str(value).strip()}")

    document = {
        "ingredient": ingredient,
        "text": "\n".join(text_parts)
    }

    documents.append(document)

# Save JSON
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(documents, f, indent=2, ensure_ascii=False)

print(f"Created {len(documents)} RAG documents.")
print(f"Saved to: {output_file}")