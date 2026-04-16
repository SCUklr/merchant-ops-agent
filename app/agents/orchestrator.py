"""Minimal orchestrator for step-01 foundation."""

from __future__ import annotations

import asyncio
import uuid
from collections.abc import AsyncGenerator

from app.schemas.chat import ChatEvent, ChatRequest


class AgentOrchestrator:
    """Minimal streaming orchestrator used in step-01."""

    async def run_stream(self, request: ChatRequest) -> AsyncGenerator[ChatEvent, None]:
        """Yield deterministic staged events for API validation."""

        trace_id = str(uuid.uuid4())

        yield ChatEvent(
            trace_id=trace_id,
            phase="intent",
            content="已识别为运营咨询请求（foundation 占位流程）。",
            meta={"intent": "general_ops_query", "user_id": request.user_id},
        )

        await asyncio.sleep(0.01)

        yield ChatEvent(
            trace_id=trace_id,
            phase="final",
            content=(
                "当前已完成最小链路联通。下一步将接入真实 RAG 与业务工具，"
                "用于规则问答、订单异常定位和工单通知。"
            ),
            meta={"session_id": request.session_id},
        )


orchestrator = AgentOrchestrator()
