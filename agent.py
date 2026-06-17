# agent.py
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import tool
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools import search_device, get_device_detail
import os

# 用内存字典模拟会话存储（生产环境换 Redis）
sessions: dict[str, ConversationBufferWindowMemory] = {}

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


def get_or_create_memory(session_id: str) -> ConversationBufferWindowMemory:
    if session_id not in sessions:
        sessions[session_id] = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            k=10  # 保留最近 10 轮对话
        )
    return sessions[session_id]


async def run_agent(message: str, session_id: str = "default") -> str:
    llm = ChatOpenAI(
        model="gpt-4o",  # 或 deepseek-chat 等兼容模型
        temperature=0.1,
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),  # 可选，用于兼容 API
    )

    tools = [search_device_tool, get_device_detail_tool]
    memory = get_or_create_memory(session_id)

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5,
    )

    result = await executor.ainvoke({"input": message})
    return result["output"]