# tools.py
import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "devices.json"

def load_devices() -> list[dict]:
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))

def search_device(query: str) -> list[dict]:
    """根据关键词搜索设备（支持位置、类型、状态）"""
    devices = load_devices()
    query_lower = query.lower()
    results = []
    for d in devices:
        if (query_lower in d["location"].lower() or
            query_lower in d["type"].lower() or
            query_lower in d["status"].lower()):
            results.append(d)
    return results

def get_device_detail(device_id: str) -> dict | None:
    """获取单个设备的完整信息"""
    devices = load_devices()
    for d in devices:
        if d["id"].upper() == device_id.upper():
            return d
    return None