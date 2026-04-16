"""Orchestrator protocol for step-02."""

from __future__ import annotations

import asyncio
import time
import uuid
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator

from app.schemas.chat import ChatEvent, ChatRequest


class BaseOrchestrator(ABC):
    """Abstract orchestrator protocol."""

    @abstractmethod
    async def run_stream(self, request: ChatRequest) -> AsyncGenerator[ChatEvent, None]:
        """Yield stage-based events for one request."""


class AgentOrchestrator(BaseOrchestrator):
    """Default orchestrator with deterministic stage protocol."""

    INTENT_RULE_QA = "rule_qa"
    INTENT_ORDER_DIAGNOSIS = "order_diagnosis"
    INTENT_EXECUTION = "execution"
    INTENT_GENERAL = "general_ops_query"

    @staticmethod
    def _classify_intent(message: str) -> tuple[str, str]:
        """Return intent and classification reason."""

        text = message.lower()

        if any(keyword in text for keyword in ["规则", "sop", "政策", "流程", "faq"]):
            return (
                AgentOrchestrator.INTENT_RULE_QA,
                "命中规则/SOP关键词",
            )

        if any(
            keyword in text
            for keyword in ["订单", "物流", "未发货", "退款", "异常", "order"]
        ):
            return (
                AgentOrchestrator.INTENT_ORDER_DIAGNOSIS,
                "命中订单异常关键词",
            )

        if any(keyword in text for keyword in ["工单", "通知", "创建", "执行", "ticket"]):
            return (
                AgentOrchestrator.INTENT_EXECUTION,
                "命中执行动作关键词",
            )

        return (
            AgentOrchestrator.INTENT_GENERAL,
            "未命中特定关键词，归类为通用运营咨询",
        )

    @staticmethod
    def _build_event(
        trace_id: str,
        phase: str,
        content: str,
        phase_start: float,
        total_start: float,
        extra_meta: dict[str, str] | None = None,
    ) -> ChatEvent:
        """Create one event with phase and total latency fields."""

        meta = {
            "phase_latency_ms": int((time.perf_counter() - phase_start) * 1000),
            "total_elapsed_ms": int((time.perf_counter() - total_start) * 1000),
        }
        if extra_meta:
            meta.update(extra_meta)
        return ChatEvent(trace_id=trace_id, phase=phase, content=content, meta=meta)

    async def run_stream(self, request: ChatRequest) -> AsyncGenerator[ChatEvent, None]:
        """Yield fixed protocol events for all requests."""

        trace_id = str(uuid.uuid4())
        total_start = time.perf_counter()
        intent, reason = self._classify_intent(request.message)

        intent_start = time.perf_counter()
        yield self._build_event(
            trace_id=trace_id,
            phase="intent",
            content=f"已识别请求意图：{intent}",
            phase_start=intent_start,
            total_start=total_start,
            extra_meta={
                "intent": intent,
                "reason": reason,
                "user_id": request.user_id,
                "session_id": request.session_id,
            },
        )

        await asyncio.sleep(0.01)

        retrieve_start = time.perf_counter()
        if intent == self.INTENT_RULE_QA:
            retrieve_content = "进入RAG检索阶段（当前为占位实现）：已准备规则/SOP检索上下文。"
        else:
            retrieve_content = "检索阶段跳过：该请求主要依赖工具调用或通用问答。"

        yield self._build_event(
            trace_id=trace_id,
            phase="retrieve",
            content=retrieve_content,
            phase_start=retrieve_start,
            total_start=total_start,
            extra_meta={"intent": intent},
        )

        await asyncio.sleep(0.01)

        tool_start = time.perf_counter()
        if intent in {self.INTENT_ORDER_DIAGNOSIS, self.INTENT_EXECUTION}:
            tool_content = (
                "进入工具阶段（当前为占位实现）："
                "将按意图路由至订单查询/工单通知工具。"
            )
        else:
            tool_content = "工具阶段跳过：当前请求无需调用业务工具。"

        yield self._build_event(
            trace_id=trace_id,
            phase="tool",
            content=tool_content,
            phase_start=tool_start,
            total_start=total_start,
            extra_meta={"intent": intent},
        )

        await asyncio.sleep(0.01)

        guard_start = time.perf_counter()
        yield self._build_event(
            trace_id=trace_id,
            phase="guard",
            content=(
                "已执行风控校验（当前为占位实现）："
                "高风险动作需满足参数完整与权限校验。"
            ),
            phase_start=guard_start,
            total_start=total_start,
            extra_meta={"risk_level": "low"},
        )

        await asyncio.sleep(0.01)

        final_start = time.perf_counter()
        yield self._build_event(
            trace_id=trace_id,
            phase="final",
            content=(
                "Step-02 编排协议已联通：本次请求输出了完整阶段轨迹"
                "（intent/retrieve/tool/guard/final）。"
            ),
            phase_start=final_start,
            total_start=total_start,
            extra_meta={"intent": intent},
        )


orchestrator = AgentOrchestrator()
