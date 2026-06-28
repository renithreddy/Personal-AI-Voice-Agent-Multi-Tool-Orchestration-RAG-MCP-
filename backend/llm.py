import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic
from tools.weather import get_weather

load_dotenv()

_client = None

def get_client():
    global _client
    if _client is None:
        _client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    return _client

# Define the weather tool for Claude
TOOLS = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a city. Use this when the user asks about weather, temperature, or climate in any location.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city name, e.g. Hyderabad, London, New York"
                }
            },
            "required": ["city"]
        }
    }
]

def get_llm_response_with_tools(message: str) -> str:
    client = get_client()

    # Step 1 — send user message + available tools to Claude
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        tools=TOOLS,
        messages=[{"role": "user", "content": message}]
    )

    # Step 2 — check if Claude wants to call a tool
    if response.stop_reason == "tool_use":
        tool_block = next(b for b in response.content if b.type == "tool_use")
        tool_name = tool_block.name
        tool_input = tool_block.input

        # Step 3 — actually call the tool
        if tool_name == "get_weather":
            tool_result = get_weather(tool_input["city"])
        else:
            tool_result = {"error": "Unknown tool"}

        # Step 4 — send result back to Claude so it can form a natural reply
        final_response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            tools=TOOLS,
            messages=[
                {"role": "user", "content": message},
                {"role": "assistant", "content": response.content},
                {
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": tool_block.id,
                        "content": json.dumps(tool_result)
                    }]
                }
            ]
        )
        return final_response.content[0].text

    # Step 5 — no tool needed, Claude answered directly
    return response.content[0].text