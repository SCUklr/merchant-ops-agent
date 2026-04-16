# Step 02 Spec - Orchestrator Protocol 与阶段事件标准化

## 1. 目标

在 Step 01 最小流式链路基础上，建立统一的编排事件协议，保证每次请求都输出完整阶段轨迹，作为后续 RAG/Tool/Guardrails 的标准插槽。

## 2. 输入 / 输出定义

### 2.1 输入

- HTTP `POST /api/v1/chat/stream`
  - `user_id: str`
  - `session_id: str`
  - `message: str`
  - `context: dict[str, str] | null`

### 2.2 输出

SSE 按固定阶段输出：

1. `intent`
2. `retrieve`
3. `tool`
4. `guard`
5. `final`
6. `done`

每个阶段事件必须包含：

- `trace_id`
- `phase`
- `content`
- `meta.phase_latency_ms`
- `meta.total_elapsed_ms`

## 3. 架构细节

- `BaseOrchestrator`：抽象协议，定义 `run_stream()` 接口。
- `AgentOrchestrator`：默认实现，包含
  - 关键词意图路由（rule_qa / order_diagnosis / execution / general）
  - 五阶段事件产出
  - 阶段耗时与总耗时埋点
- `ChatPhase`：在 schema 层收敛为 Literal，防止事件类型漂移。

## 4. Prompt 与策略示例

当前阶段采用规则意图路由（非 LLM 分类）：

1. 命中“规则/SOP/FAQ” -> `rule_qa`
2. 命中“订单/物流/退款/异常” -> `order_diagnosis`
3. 命中“工单/通知/执行” -> `execution`
4. 其他 -> `general_ops_query`

## 5. 代码变更范围

```text
app/
├── agents/orchestrator.py      # BaseOrchestrator + 默认实现
├── api/v1/chat.py              # done事件 trace_id 对齐
└── schemas/chat.py             # ChatPhase 枚举化
tests/
└── test_health_api.py          # 验证完整阶段协议与trace一致性
```

## 6. 验收标准

- `POST /api/v1/chat/stream` 返回 6 个阶段事件，顺序固定。
- 所有事件共享同一个 `trace_id`。
- 每个阶段都具备 `phase_latency_ms` 与 `total_elapsed_ms`。
- `pytest tests/test_health_api.py` 全通过。

## 7. 风险与缓解

- 风险：阶段协议后续扩展导致前端兼容问题。  
  缓解：固定 phase 集合，新增阶段需版本化。
- 风险：意图规则误判。  
  缓解：后续 Step 3/4 接入 LLM 分类器 + 回放评测对比。

## 8. 本步骤简历成果点

- 设计并落地 Agent 编排阶段协议（intent/retrieve/tool/guard/final），实现流式可观测链路。
- 建立 trace_id 与阶段耗时埋点，为后续评测、回归与性能优化提供数据基础。
- 通过 schema 枚举化和测试约束，保证事件协议稳定演进。
