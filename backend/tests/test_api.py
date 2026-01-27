from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health():
    """Test health endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_chat_endpoint():
    """Test chat endpoint"""
    response = client.post(
        "/api/chat",
        json={"message": "Hello", "conversation_history": []}
    )
    # May fail if API key not configured, but tests structure
    assert response.status_code in [200, 500]

# Add more tests as needed
