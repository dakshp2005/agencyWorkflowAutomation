import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found in .env")
    exit(1)

genai.configure(api_key=api_key)

def test_model(model_name):
    print(f"Testing model: {model_name}")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Give me a JSON object with one key 'status' and value 'ok'. Return ONLY JSON.")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error with {model_name}: {e}")

test_model("gemini-1.5-flash")
test_model("gemini-2.5-flash")
