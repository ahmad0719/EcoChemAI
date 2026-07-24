from google import genai
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv(Path(".env"))

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

for model in client.models.list():
    print(model.name)
