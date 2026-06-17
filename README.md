![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![LangChain](https://img.shields.io/badge/LangChain-0.2+-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)
```mermaid
graph TD
    U[用户] --> G[Gradio]
    G --> F[FastAPI]
    F --> A[LangChain Agent]
    A --> L[LLM]
    A --> T[工具函数]
```
<details>
<summary>点击展开：完整的 API 文档</summary>

## API 文档
| 接口 | 方法 | 说明 |
|------|------|------|
| /chat | POST | 对话接口 |
| /health | GET | 健康检查 |

</details>
