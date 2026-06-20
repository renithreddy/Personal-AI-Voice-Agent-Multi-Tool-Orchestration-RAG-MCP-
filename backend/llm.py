import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

_client = None

def get_client():
    if _client is None:
        _client = genai.Client( api_key = os.load_dotenv("GEMINI_API_KEY") )
    return _client

def get_llm_response(message : str) -> str:
    client = get_client()
    response = client.models.generate_contents(
        model = "gemini-3.5-flash",
        contents = message
    )
    return response