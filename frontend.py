# frontend.py
import gradio as gr
import requests

BACKEND_URL = "http://localhost:8000/chat"

def chat_fn(message: str, history: list):
    resp = requests.post(BACKEND_URL, json={"message": message})
    return resp.json()["reply"]

demo = gr.ChatInterface(
    fn=chat_fn,
    title="智能设备管理助手",
    description="用自然语言查询和管理物联网设备",
    examples=[
        "北京机房有哪些设备？",
        "哪些设备处于报警状态？",
        "帮我查看 BJ-001 的详细信息",
    ],
)

if __name__ == "__main__":
    demo.launch()