from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    """Проверка корневого эндпоинта"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health():
    """Проверка эндпоинта здоровья"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"