from fastapi import FastAPI
from pydantic import BaseModel
from llm import get_llm_response

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "Agent backend is running"}

@app.post("/chat")
def chat(request: ChatRequest):
    reply = get_llm_response(request.message)
    return {"reply": reply}