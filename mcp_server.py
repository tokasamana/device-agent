# mcp_server.py
from fastmcp import FastMCP
from tools import search_device, get_device_detail

mcp = FastMCP("Device Manager")

@mcp.tool()
def search_device_mcp(query: str) -> str:
    """搜索设备，支持按位置、类型、状态过滤"""
    results = search_device(query)
    if not results:
        return f"未找到匹配 '{query}' 的设备"
    lines = [f"找到 {len(results)} 台设备："]
    for d in results:
        lines.append(f"  - {d['id']}: {d['type']} @ {d['location']} [{d['status']}]")
    return "\n".join(lines)

@mcp.tool()
def get_device_detail_mcp(device_id: str) -> str:
    """获取指定设备的完整详情"""
    device = get_device_detail(device_id)
    if device is None:
        return f"设备 '{device_id}' 不存在"
    lines = [f"设备 {device['id']} 详情："]
    for k, v in device.items():
        lines.append(f"  {k}: {v}")
    return "\n".join(lines)

if __name__ == "__main__":
    mcp.run()