from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_status_and_kets():
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200

    body = resp.json()
    assert set(body.keys()) == {"status", "version", "time_utc"}

    assert body["status"] == "ok"
    assert isinstance(body["version"], str)
    assert isinstance(body["time_utc"], str)
