# Step 01 Spec - Foundation Skeleton 与最小 API

## 1. 目标

在保留当前仓库的前提下，借鉴成熟多 Agent 工程分层，完成可运行的后端骨架与最小流式 API，为后续 RAG/Tools 链路提供稳定入口。

## 2. 输入 / 输出定义

### 2.1 输入

- HTTP `GET /`
- HTTP `GET /api/v1/health`
- HTTP `POST /api/v1/chat/stream`
  - body:
    - `user_id: str`
    - `session_id: str`
    - `message: str`
    - `context: dict[str, str] | null`

### 2.2 输出

- 根路由与健康检查返回 JSON 状态。
- 流式接口返回 SSE `data: {...}`，阶段包含：
  - `intent`
  - `final`
  - `done`

## 3. 架构细节

- `app/main.py`：FastAPI 生命周期与路由装配。
- `app/api/v1/chat.py`：SSE 编码与流式响应。
- `app/agents/orchestrator.py`：最小编排器（后续替换为 LangGraph/ReAct）。
- `app/schemas/chat.py`：请求和事件 schema。
- `app/core/*`：配置与日志。

## 4. Prompt 示例（当前阶段）

系统提示（最小版）：

1. 你是电商商家运营助手。
2. 当前阶段不执行真实工具，仅返回结构化占位结果。
3. 输出必须包含 intent 与建议动作。

## 5. 代码结构

```text
app/
├── api/v1/chat.py
├── api/v1/health.py
├── agents/orchestrator.py
├── core/config.py
├── core/logging.py
├── main.py
└── schemas/chat.py
tests/
└── test_health_api.py
```

## 6. 验收标准

- `uvicorn app.main:app --reload` 可启动。
- `GET /api/v1/health` 返回 `{"status":"ok"}`。
- `POST /api/v1/chat/stream` 可以收到连续 SSE 事件并结束于 `done`。
- `pytest tests/test_health_api.py` 通过。

## 7. 风险与缓解

- 风险：SSE 格式错误导致前端无法消费。
  - 缓解：统一 `encode_sse_event()` 方法，并写流式解析测试。
- 风险：后续扩展造成 schema 演化混乱。
  - 缓解：先固定 `ChatRequest` 与 `ChatEvent` 模型。

## 8. 本步骤简历成果点

- 独立完成生产化后端骨架搭建，落地 FastAPI + SSE 实时响应能力。
- 以 Spec-Driven 方式固化输入输出契约与阶段事件协议，为后续 Agent/RAG/Tools 扩展建立稳定基座。
