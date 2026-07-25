import streamlit as st
import re
from app.ocr import extract_text
from app.api import analyze
from app.search import search_ingredient
from app.llm import ask_llm
from app.prompts import SYSTEM_PROMPT


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
uploaded_file = st.file_uploader(
    "📷 Upload an ingredient label",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    with open("temp.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())

    text = extract_text("temp.jpg")

    st.subheader("Detected Text")
    st.write(text)

    # Extract ingredient list from OCR text
    ingredients = []

    if "ACTIVE INGREDIENTS:" in text.upper():
        ingredient_text = text.upper().split("ACTIVE INGREDIENTS:")[1]

        # Replace common separators with commas
        ingredient_text = re.sub(r"[&;]", ",", ingredient_text)

        # Split into individual ingredients
        ingredients = [
            i.strip().title()
            for i in ingredient_text.split(",")
            if i.strip()
        ]

        # Remove obvious non-ingredient words
        ingredients = [
            i for i in ingredients
            if i.lower() not in ["day", "directions of use"]
        ]

    if ingredients:
        st.subheader("AI Ingredient Analysis")

        for ingredient in ingredients:
            st.markdown(f"### {ingredient}")
            st.write(analyze(ingredient))
    else:
        st.warning("No ingredient list detected.")
