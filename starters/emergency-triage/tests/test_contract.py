"""Contract test: the shape other teams rely on. If this breaks, you broke someone else."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json()["status"] == "ok"


def test_endpoint_responds():
    res = client.post("/triage", json={})
    assert res.status_code == 200, res.text
    assert "method" in res.json()
