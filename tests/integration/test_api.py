from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()


def test_ingest_and_query():
    ingest_resp = client.post(
        "/ingest",
        json={"content": "FastAPI is awesome"}
    )
    assert ingest_resp.status_code == 200

    query_resp = client.post(
        "/query",
        json={"query": "What is FastAPI?"}
    )
    assert query_resp.status_code == 200

    body = query_resp.json()
    assert "final_answer" in body
