# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # 读取 .env 文件

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

# 启动时检查，避免跑到一半才发现没配
if not OPENAI_API_KEY:
    raise ValueError("请在 .env 文件中设置 OPENAI_API_KEY")