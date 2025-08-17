import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(dotenv_path='secrets.env')

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def generate_from_ai(prompt: str) -> str | None:
    """
        Handles communication with the Gemini API.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()
        return None
    
    except Exception as e:
        print(f"Error using Gemini API: {e}")
        return None