from pathlib import Path
from dotenv import load_dotenv
from google import genai
import os

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def ask_llm(prompt):
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
    )
    return response.text



