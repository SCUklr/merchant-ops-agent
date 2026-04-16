"""Schemas for chat APIs."""

from typing import Any
from typing import Literal

from pydantic import BaseModel, Field

ChatPhase = Literal["intent", "retrieve", "tool", "guard", "final", "done"]


class ChatRequest(BaseModel):
    """Input payload for streaming chat."""

    user_id: str = Field(..., min_length=1)
    session_id: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)
    context: dict[str, str] | None = None


class ChatEvent(BaseModel):
    """SSE event payload."""

    trace_id: str
    phase: ChatPhase
    content: str
    meta: dict[str, Any] = Field(default_factory=dict)
