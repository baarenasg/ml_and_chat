import pytest
from fastapi.testclient import TestClient
from RAG.chat import app

client = TestClient(app)

def test_read_main():
    response = client.get("/v1/models")
    assert response.status_code == 200
    assert "data" in response.json()

def test_chat_endpoint():
    response = client.post("/api/chat", json={"messages": [{"content": "hello"}]})
    assert response.status_code == 200
    assert "message" in response.json()
    assert "content" in response.json()["message"]
