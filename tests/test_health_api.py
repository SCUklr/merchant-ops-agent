"""Step-01 API health tests."""

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
    """Stream endpoint should emit staged SSE payloads."""

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
    assert '"phase": "intent"' in response.text
    assert '"phase": "final"' in response.text
    assert '"phase": "done"' in response.text
