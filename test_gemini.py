from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

for model in ["gemini-3.5-flash-lite", "gemini-3.8-flash"]:
    try:
        response = client.models.generate_content(model=model, contents="Say hello in one word.")
        print(f"SUCCESS {model}: {response.text.strip()}")
    except Exception as e:
        print(f"FAILED {model}: {e}")
