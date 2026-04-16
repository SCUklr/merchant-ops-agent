# 电商智能客服 AI Agent 八步开发计划

## Step 1 - Foundation Skeleton（第 1 小时）

- 目标：迁移成熟工程结构，跑通最小 FastAPI + SSE API。
- 交付：
  - `app/` 分层目录与基础模块
  - `GET /` 与 `GET /api/v1/health`
  - `POST /api/v1/chat/stream` 最小流式输出
- 验收：本地启动成功，健康检查与流式返回通过。

## Step 2 - Orchestrator Protocol

- 目标：建立统一编排协议，输出分阶段事件。
- 交付：
  - `intent/retrieve/tool/guard/final` 事件协议
  - `AgentOrchestrator` 抽象与默认实现
- 验收：同一输入可输出完整阶段轨迹。

## Step 3 - 商品规则问答 RAG

- 目标：完成规则/SOP/FAQ 检索问答闭环。
- 交付：
  - 文档切分、索引、召回、重排
  - 证据引用与来源输出
- 验收：离线样例可返回证据支撑答案。

## Step 4 - 订单异常定位（Tool + Rule Check）

- 目标：接通订单查询与异常归因流程。
- 交付：
  - `query_order_status` 工具
  - 异常类型判定与规则校验
- 验收：给出异常原因、建议和限制条件。

## Step 5 - 工单创建与通知（Function Calling）

- 目标：自然语言触发执行动作闭环。
- 交付：
  - `create_ticket`、`push_notification` 工具
  - 调用计划、执行回执、失败回退
- 验收：生成工单号与通知结果。

## Step 6 - Memory + Cache + Fallback

- 目标：提升稳定性和多轮体验。
- 交付：
  - 会话记忆摘要
  - 热问题缓存
  - 模型/工具失败回退
- 验收：重复问题响应加速，异常可降级返回。

## Step 7 - Evaluation & Smoke

- 目标：建立可回放、可对比的评测流程。
- 交付：
  - 10-20 条评测 case
  - smoke 脚本 + 回归统计
- 验收：输出成功率、命中率、耗时。

## Step 8 - Metrics & Interview Pack

- 目标：沉淀可自证成果与面试材料。
- 交付：
  - 指标口径文档
  - 迭代记录与关键 trade-off
  - 简历版本（保守版/数据版）
- 验收：可在 10 分钟内完成项目讲解与深问答辩。
