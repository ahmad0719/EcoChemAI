from app.search import search_ingredient
from app.llm import ask_llm
from app.prompts import SYSTEM_PROMPT

def analyze(name):
    df = search_ingredient(name)

    if df.empty:
        return "Ingredient not found in the EcoChemAI database."

    context = df.to_string(index=False)

    prompt = f"""
{SYSTEM_PROMPT}

Use ONLY the information provided below.

Database Results:

{context}

User Query:
{name}

If the database does not contain enough information, clearly state that instead of making assumptions.
"""

    return ask_llm(prompt)
