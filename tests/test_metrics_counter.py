from app.main import app
from fastapi.testclient import TestClient
import re


client = TestClient(app)


def test_http_requests_total_counter_increments():
    health_request = client.get("api/v1/health")
    assert health_request.status_code == 200

    metrics_request = client.get("/metrics")
    assert metrics_request.status_code == 200

    metrics_body = metrics_request.text

    assert re.search(r"\bhttp_requests_total\b", metrics_body)

    assert re.search(
        r'http_requests_total\{[^}]*path="/api/v1/health"[^}]*status="200"[^}]*\}\s+\d+(\.0)?',
        metrics_body,
    )
