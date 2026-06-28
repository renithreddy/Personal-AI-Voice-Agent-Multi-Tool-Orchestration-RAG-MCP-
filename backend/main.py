from fastapi import FastAPI
from pydantic import BaseModel
from llm import get_llm_response_with_tools
import json

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "Agent backend is running"}

@app.post("/chat")
def chat(request: ChatRequest):
    reply = get_llm_response_with_tools(request.message)
    return {"reply": reply}