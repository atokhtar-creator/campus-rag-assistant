from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_known_question_returns_source():
    response = client.post(
        "/ask",
        json={"question": "How can I reset my university password?"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["sources"]
    assert "password" in body["sources"][0]["title"].lower()
