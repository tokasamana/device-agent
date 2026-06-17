# agent.py
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
from tools import search_device, get_device_detail
import os
from dotenv import load_dotenv
# 加载 .env 文件
load_dotenv()

# 用内存字典模拟会话存储（生产环境换 Redis）
sessions: dict[str, list] = {}

SYSTEM_PROMPT = """你是一个智能设备管理助手。你可以帮助用户查询和管理物联网设备。

可用的工具：
- search_device: 根据关键词（位置/类型/状态）搜索设备
- get_device_detail: 根据设备ID获取详细信息

工作原则：
1. 当用户提出复杂需求时，先分解为子任务再逐步执行
2. 如果某步失败，尝试其他方案或告知用户
3. 回答要简洁准确，涉及设备数据时列出关键信息
4. 如果需要用户确认的操作（如重启设备），先说明影响范围
"""

@tool
def search_device_tool(query: str) -> str:
    """搜索设备，支持按位置、类型、状态过滤。query 可以是 '北京'、'报警'、'温度传感器' 等"""
    results = search_device(query)
    if not results:
        return f"未找到匹配 '{query}' 的设备"
    lines = [f"找到 {len(results)} 台设备："]
    for d in results:
        lines.append(f"  - {d['id']}: {d['type']} @ {d['location']} [{d['status']}]")
    return "\n".join(lines)

@tool
def get_device_detail_tool(device_id: str) -> str:
    """获取指定设备的完整详情，device_id 如 'BJ-001'"""
    device = get_device_detail(device_id)
    if device is None:
        return f"设备 '{device_id}' 不存在"
    lines = [f"设备 {device['id']} 详情："]
    for k, v in device.items():
        lines.append(f"  {k}: {v}")
    return "\n".join(lines)


def get_or_create_memory(session_id: str) -> list:
    if session_id not in sessions:
        sessions[session_id] = []
    return sessions[session_id]


async def run_agent(message: str, session_id: str = "default") -> str:
    llm = ChatOpenAI(
        model="deepseek-v4-flash",  # 或 deepseek-chat 等兼容模型
        temperature=0.1,
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),  # 可选，用于兼容 API
    )

    tools = [search_device_tool, get_device_detail_tool]
    memory = get_or_create_memory(session_id)

    # 组装完整消息：系统提示 + 历史对话 + 当前用户输入
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=None)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + memory + [{"role": "user", "content": message}]
    
    # 异步调用，可设置最大迭代次数等配置
    response = await agent.ainvoke(
        {"messages": messages},
        config={"max_iterations": 5}   # 防止无限循环
    )
    # 提取最后一条助手消息（最终回复）
    assistant_msg = response["messages"][-1]
    reply = assistant_msg.content

    # 更新历史：记录用户消息和助手回复
    memory.append({"role": "user", "content": message})
    memory.append({"role": "assistant", "content": reply})

    # 控制历史长度（可选，避免 session 无限膨胀）
    if len(memory) > 20:
        sessions[session_id] = memory[-20:]

    return reply