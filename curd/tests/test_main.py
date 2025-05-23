import pytest
from fastapi.testclient import TestClient
from main import app, messages_list


@pytest.fixture
def client():
    # Clear the messages list before each test
    messages_list.clear()
    with TestClient(app) as client:
        yield client


def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello"}


def test_about_route(client):
    response = client.get("/about")
    assert response.status_code == 200
    assert response.json() == {"message": "This is the about page."}


def test_create_message(client):
    # Test creating a message
    response = client.post(
        "/messages/",
        json={"msg_name": "Test Message", "content": "This is a test message"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["msg_id"] == 1
    assert data["data"]["msg_name"] == "Test Message"
    assert data["data"]["content"] == "This is a test message"


def test_get_all_messages(client):
    # Create two messages
    client.post("/messages/", json={"msg_name": "Message 1", "content": "Content 1"})
    client.post("/messages/", json={"msg_name": "Message 2", "content": "Content 2", "is_active": False})
    
    # Test getting all messages
    response = client.get("/messages/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) == 2
    
    # Test filtering active messages
    response = client.get("/messages/?active_only=true")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert list(data["data"].values())[0]["msg_name"] == "Message 1"


def test_get_message(client):
    # Create a message
    client.post("/messages/", json={"msg_name": "Test Get", "content": "Get content"})
    
    # Test getting the message
    response = client.get("/messages/1")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["msg_name"] == "Test Get"
    
    # Test getting non-existent message
    response = client.get("/messages/999")
    assert response.status_code == 404


def test_update_message(client):
    # Create a message
    client.post("/messages/", json={"msg_name": "Original", "content": "Original content"})
    
    # Update the message
    response = client.put(
        "/messages/1",
        json={"msg_name": "Updated", "content": "Updated content"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["msg_name"] == "Updated"
    assert data["data"]["content"] == "Updated content"
    
    # Test updating non-existent message
    response = client.put(
        "/messages/999",
        json={"msg_name": "Not Found", "content": "This won't be created"}
    )
    assert response.status_code == 404


def test_delete_message(client):
    # Create a message
    client.post("/messages/", json={"msg_name": "To Delete", "content": "Will be deleted"})
    
    # Delete the message
    response = client.delete("/messages/1")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["msg_name"] == "To Delete"
    
    # Verify message is deleted
    response = client.get("/messages/1")
    assert response.status_code == 404
    
    # Test deleting already deleted message
    response = client.delete("/messages/1")
    assert response.status_code == 404
