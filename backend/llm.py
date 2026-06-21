import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

_client = None

def get_client():
    global _client
    if _client is None:
        _client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    return _client

def get_llm_response(message: str) -> str:
    client = get_client()
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": message}
        ]
    )
    return response.content[0].text