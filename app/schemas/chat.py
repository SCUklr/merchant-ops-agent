"""Schemas for chat APIs."""

from typing import Any

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Input payload for streaming chat."""

    user_id: str = Field(..., min_length=1)
    session_id: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)
    context: dict[str, str] | None = None


class ChatEvent(BaseModel):
    """SSE event payload."""

    trace_id: str
    phase: str
    content: str
    meta: dict[str, Any] = Field(default_factory=dict)
