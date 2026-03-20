from fastapi.testclient import TestClient
import sys
import os

# Add the project folder to the Python path
# This helps the test find our 'app' folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

# Create a Test Client
client = TestClient(app)

def test_read_root():
    """
    Test if the home page works.
    We expect a status code 200 (OK).
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]

def test_health_check():
    """
    Test if the system is healthy.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_chat_endpoint_structure():
    """
    Test if the chat API returns the correct JSON structure.
    Note: We send a simple message to check the format.
    """
    payload = {
        "message": "Hello AI",
        "model_name": "gpt-4o"
    }
    # We use a timeout because AI can be slow
    response = client.post("/api/v1/chat/send", json=payload)
    
    # Check if the response is correct
    assert response.status_code == 200
    data = response.json()
    assert "user_message" in data
    assert "ai_response" in data
    assert "performance" in data