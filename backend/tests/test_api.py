from fastapi.testclient import TestClient

from app import vroom
from app.main import app

from app.settings import settings

client = TestClient(app)


def test_optimize_returns_our_format(monkeypatch, problem, vroom_answer):
    async def fake_call_vroom(payload):
        return vroom_answer

    monkeypatch.setattr(vroom, "call_vroom", fake_call_vroom)

    response = client.post("/api/v1/optimize", json=problem)

    assert response.status_code == 200
    body = response.json()
    assert body["routes"][0]["steps"][1]["jobId"] == 1
    assert body["unassigned"][0]["jobId"] == 2
    assert body["summary"]["distance"] == 1000  # the fake's made-up number: VROOM was never called


def test_bad_latitude_gives_422(problem):
    problem["jobs"][0]["location"]["lat"] = 200

    response = client.post("/api/v1/optimize", json=problem)

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "jobs", 0, "location", "lat"]


def test_vroom_down_gives_502(monkeypatch, problem):
    # Nothing listens on port 1, so this is what "VROOM is down" looks like
    monkeypatch.setattr(settings, "vroom_url", "http://localhost:1")

    response = client.post("/api/v1/optimize", json=problem)

    assert response.status_code == 502
    assert response.json()["source"] == "vroom"

def test_health_says_ok():
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_cors_allows_the_frontend():
    response = client.get("/api/v1/health", headers={"Origin": "http://localhost:5173"})

    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_cors_ignores_other_websites():
    response = client.get("/api/v1/health", headers={"Origin": "https://evil.example"})

    assert "access-control-allow-origin" not in response.headers

def test_json_uses_camel_case(monkeypatch, problem, vroom_answer):
    async def fake_call_vroom(payload):
        return vroom_answer

    monkeypatch.setattr(vroom, "call_vroom", fake_call_vroom)

    body = client.post("/api/v1/optimize", json=problem).json()

    assert "vehicleId" in body["routes"][0]
    assert "vehicle_id" not in body["routes"][0]
