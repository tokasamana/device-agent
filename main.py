# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from agent import run_agent

app = FastAPI(title="Device Management Agent")

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    reply = await run_agent(request.message, request.session_id)
    return ChatResponse(reply=reply)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)