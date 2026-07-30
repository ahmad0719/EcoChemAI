from pathlib import Path
import pandas as pd
import requests
import time
from urllib.parse import quote

# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

input_file = DATA_DIR / "ingredient_database_1000.csv"
output_file = DATA_DIR / "ingredient_database_enriched.csv"

# Load original database
df = pd.read_csv(input_file)

# Make sure new columns can accept text
new_columns = [
    "PubChem CID",
    "IUPAC Name",
    "Molecular Formula",
    "Molecular Weight",
    "PubChem Match"
]

for col in new_columns:
    if col not in df.columns:
        df[col] = pd.Series([None] * len(df), dtype="object")
    else:
        df[col] = df[col].astype("object")


def get_pubchem_data(ingredient):

    encoded_name = quote(str(ingredient).strip())

    url = (
        "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"
        f"{encoded_name}/property/"
        "IUPACName,MolecularFormula,MolecularWeight/JSON"
    )

    try:
        response = requests.get(url, timeout=20)

        if response.status_code != 200:
            print(f"   PubChem HTTP status: {response.status_code}")
            return None

        data = response.json()
        properties = data["PropertyTable"]["Properties"][0]

        return {
            "PubChem CID": str(properties.get("CID", "")),
            "IUPAC Name": str(properties.get("IUPACName", "")),
            "Molecular Formula": str(properties.get("MolecularFormula", "")),
            "Molecular Weight": str(properties.get("MolecularWeight", "")),
            "PubChem Match": "Found"
        }

    except Exception as e:
        print(f"   Error: {e}")
        return None


print(f"Total ingredients: {len(df)}")
print("Starting PubChem enrichment...\n")

for index, row in df.iterrows():

    ingredient = str(row["Ingredient"]).strip()

    print(f"[{index + 1}/{len(df)}] {ingredient}")

    result = get_pubchem_data(ingredient)

    if result:
        for column, value in result.items():
            df.at[index, column] = value

        print("   ✓ PubChem match found")

    else:
        df.at[index, "PubChem Match"] = "Not Found"
        print("   ✗ No PubChem match")

    # PubChem asks users not to exceed 5 requests/second
    time.sleep(0.25)


df.to_csv(output_file, index=False)

print("\n--------------------------------")
print("Enrichment completed!")
print(f"Saved to: {output_file}")
print("--------------------------------")



