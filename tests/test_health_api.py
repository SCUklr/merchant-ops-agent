"""Step-01 API health tests."""

import json

from fastapi.testclient import TestClient

from app.main import app


def test_root_endpoint() -> None:
    """Root endpoint should return service metadata."""

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "merchant-ops-agent"


def test_health_endpoint() -> None:
    """Health endpoint should return ok status."""

    client = TestClient(app)
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_stream_endpoint() -> None:
    """Stream endpoint should emit full stage protocol."""

    client = TestClient(app)
    response = client.post(
        "/api/v1/chat/stream",
        json={
            "user_id": "u_001",
            "session_id": "s_001",
            "message": "测试一下最小流式链路",
        },
    )
    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]

    events: list[dict] = []
    for raw_line in response.text.splitlines():
        if not raw_line.startswith("data: "):
            continue
        payload = raw_line.removeprefix("data: ").strip()
        events.append(json.loads(payload))

    phases = [event["phase"] for event in events]
    assert phases == ["intent", "retrieve", "tool", "guard", "final", "done"]

    request_trace_id = events[0]["trace_id"]
    assert request_trace_id != "system"
    assert all(event["trace_id"] == request_trace_id for event in events)

    for phase_event in events[:-1]:
        assert "phase_latency_ms" in phase_event["meta"]
        assert "total_elapsed_ms" in phase_event["meta"]
