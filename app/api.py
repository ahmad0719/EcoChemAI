from search import search_ingredient
from llm import ask_llm
from prompts import SYSTEM_PROMPT

def analyze(name):
    df = search_ingredient(name)

    if df.empty:
        return "Ingredient not found."

    ingredient = df.iloc[0].to_dict()

    prompt = f"""
{SYSTEM_PROMPT}

Ingredient information:

{ingredient}

Explain this ingredient.
"""

    return ask_llm(prompt)
