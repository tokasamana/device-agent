# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from agent import run_agent
from tools import load_devices, search_device, get_device_detail
app = FastAPI(
    title="Device Management Agent",
    description="智能设备管理助手 API",
    version="v1",
    )

# 定义请求体的"形状"
class ChatRequest(BaseModel):
    message: str = Field(..., description="用户消息", min_length=1)
    session_id: str = Field("default", description="会话ID")

# 定义响应体的"形状"
class ChatResponse(BaseModel):
    reply: str = Field(..., description="Agent 的回复")
    session_id: str = Field("default")
    tokens_used: int = 0

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    reply = await run_agent(request.message, request.session_id)
    return ChatResponse(
        reply=reply,
        session_id=request.session_id,
        )

@app.post("/devices")             # POST - 创建数据
def create_device(device: dict):
    # 存入数据库...
    return {"status": "created"}

@app.get("/devices")              # GET  - 查询数据
def get_devices():
    devices = load_devices()
    return devices

# 路径参数：URL 的一部分
@app.get("/devices/{device_id}")
def get_device(device_id: str):        # ← 路径参数
    devices = load_devices()
    for i in devices:
        if i["id"] == device_id:
            return i
    raise HTTPException(status_code=404, detail=f"Device {device_id} not found")
# 访问：GET /devices/BJ-001

@app.get("/")
async def root():
    return {"message": "Device Agent API is running", "docs": "/docs"}

@app.get("/health")
async def health():
    """健康检查接口"""
    return {"msg": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)