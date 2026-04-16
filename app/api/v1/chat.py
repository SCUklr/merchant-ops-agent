"""Streaming chat API."""

from __future__ import annotations

import json
from collections.abc import AsyncGenerator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.agents.orchestrator import orchestrator
from app.schemas.chat import ChatEvent, ChatRequest

router = APIRouter(prefix="/chat", tags=["chat"])


def encode_sse_event(event: ChatEvent) -> str:
    """Serialize event as standard SSE data frame."""

    data = json.dumps(event.model_dump(), ensure_ascii=False)
    return f"data: {data}\n\n"


async def stream_events(payload: ChatRequest) -> AsyncGenerator[str, None]:
    """Yield SSE events for the request."""

    async for event in orchestrator.run_stream(payload):
        yield encode_sse_event(event)

    done_event = ChatEvent(
        trace_id="system",
        phase="done",
        content="stream finished",
        meta={},
    )
    yield encode_sse_event(done_event)


@router.post("/stream")
async def chat_stream(payload: ChatRequest) -> StreamingResponse:
    """Return streamed chat events."""

    return StreamingResponse(
        stream_events(payload),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
