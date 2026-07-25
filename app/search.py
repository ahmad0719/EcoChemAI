from rapidfuzz import process
import pandas as pd
from app.database import engine


def search_ingredient(name):

    # Load the ingredients table
    df = pd.read_sql(
        "SELECT * FROM ingredients",
        engine
    )

    # 1. Exact match
    result = df[
        df["ingredient"].str.contains(
            name,
            case=False,
            na=False
        )
    ]

    if not result.empty:
        return result

    # 2. Fuzzy match
    matches = process.extract(
        name,
        df["ingredient"].tolist(),
        limit=3
    )

    if matches:
        ingredient_name = matches[0][0]
        score = matches[0][1]

        print(f"Fuzzy match: {ingredient_name} ({score}%)")

        if score >= 70:
            return df[
                df["ingredient"] == ingredient_name
            ]

    return pd.DataFrame()
    
