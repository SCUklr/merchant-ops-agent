# AI 商家运营助手 Agent

面向电商商家运营场景的生产级 AI Agent 项目，采用 Spec-Driven + Step-by-Step 方式建设，目标是将问题处理流程标准化为：

`检索 -> 分析 -> 执行 -> 校验`

## 当前状态

- 已完成 Step 01：基础工程骨架 + 最小 FastAPI/SSE API
- 待完成 Step 02-08：编排协议、RAG、工具链、评测、指标沉淀

详细规格见：

- `PROJECT_TECH_DOC.md`
- `docs/DEVELOPMENT_PLAN_8_STEPS.md`
- `docs/specs/step-01-foundation.md`
- `docs/电商智能客服AI-Agent系统设计技术方案（完整版）.md`
- `docs/电商智能客服AI-Agent系统设计技术方案（豆包精简版）.md`

## 快速启动

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 最小 API 验证

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/api/v1/health
```

```bash
curl -N -X POST "http://127.0.0.1:8000/api/v1/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id":"u_001",
    "session_id":"s_001",
    "message":"帮我看看订单异常怎么处理",
    "context":{"channel":"merchant_console"}
  }'
```

## 测试

```bash
pytest tests/test_health_api.py
```
