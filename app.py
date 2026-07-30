import streamlit as st
import re

from app.ocr import extract_text
from app.api import analyze
from app.search import search_ingredient

st.set_page_config(
    page_title="EcoChemAI",
    page_icon="🧪",
    layout="centered"
)

st.title("🧪 EcoChemAI")
st.subheader("AI-Powered Ingredient Safety Analyzer")


# -----------------------------
# Manual ingredient analysis
# -----------------------------

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

            with st.spinner("Retrieving knowledge and analyzing..."):
                explanation = analyze(ingredient)

            st.markdown("---")
            st.markdown(explanation)


# -----------------------------
# Image / OCR analysis
# -----------------------------

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

        ingredient_text = text.upper().split(
            "ACTIVE INGREDIENTS:"
        )[1]

        # Replace common separators with commas
        ingredient_text = re.sub(
            r"[&;]",
            ",",
            ingredient_text
        )

        # Split into individual ingredients
        ingredients = [
            i.strip().title()
            for i in ingredient_text.split(",")
            if i.strip()
        ]

        # Remove obvious non-ingredient words
        ingredients = [
            i
            for i in ingredients
            if i.lower() not in [
                "day",
                "directions of use"
            ]
        ]

    if ingredients:

        st.subheader("AI Ingredient Analysis")

        for ingredient in ingredients:

            st.markdown(f"### {ingredient}")

            with st.spinner(
                f"Retrieving knowledge for {ingredient}..."
            ):
                result = analyze(ingredient)

            st.write(result)

    else:

        st.warning("No ingredient list detected.")
