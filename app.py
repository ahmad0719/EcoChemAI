import streamlit as st

from app.search import search_ingredient
from app.llm import ask_llm

st.set_page_config(
    page_title="EcoChemAI",
    page_icon="🧪",
    layout="centered"
)

st.title("🧪 EcoChemAI")
st.subheader("AI-Powered Ingredient Safety Analyzer")

ingredient = st.text_input("Enter an ingredient name")

if st.button("Analyze"):

    if ingredient.strip() == "":
        st.warning("Please enter an ingredient.")
    else:

        result = search_ingredient(ingredient)

        if result.empty:
            st.error("Ingredient not found in database.")

        else:

            st.success("Ingredient found!")

            st.dataframe(result)

            prompt = f"""
You are EcoChemAI, an expert Chemical Engineer.

Explain this ingredient in simple language.

Ingredient:
{ingredient}

Include:

1. Function
2. Health Concerns
3. Environmental Impact
4. Safer Alternatives
5. Safety Rating (1-10)
"""

            with st.spinner("Analyzing..."):
                explanation = ask_llm(prompt)

            st.markdown("---")
            st.markdown(explanation)