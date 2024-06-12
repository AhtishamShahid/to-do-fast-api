import pytest
from fastapi.testclient import TestClient
from main import app
from app.database import Base, engine, SessionLocal

# Create a TestClient for the FastAPI app
client = TestClient(app)


@pytest.fixture(scope="module")
def test_db():
    """
    Fixture to create and drop the test database for the duration of the tests.
    """
    # Create the database and the tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop the tables and the database
    Base.metadata.drop_all(bind=engine)


def test_create_todo_item(test_db):
    """
    Test creating a new todo item.
    """
    response = client.post("/todos/", json={"title": "Test Todo", "description": "This is a test"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["description"] == "This is a test"
    assert "id" in data
    assert data["completed"] is False


def test_read_todo_item(test_db):
    """
    Test reading a todo item by its ID.
    """
    response = client.post("/todos/", json={"title": "Test Todo", "description": "This is a test"})
    assert response.status_code == 200
    todo_id = response.json()["id"]

    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Test Todo"
    assert data["description"] == "This is a test"
    assert data["completed"] is False


def test_delete_todo_item(test_db):
    """
    Test deleting a todo item.
    """
    response = client.post("/todos/", json={"title": "Test Todo", "description": "This is a test"})
    assert response.status_code == 200
    todo_id = response.json()["id"]

    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["detail"] == "Todo deleted"

    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Todo not found"
