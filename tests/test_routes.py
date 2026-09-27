import pytest

from app import create_app, db
from app.models import Task


@pytest.fixture()
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_create_task(client):
    response = client.post(
        "/api/tasks",
        json={
            "title": "Test Jenkins Pipeline",
            "description": "Automated API test",
            "priority": "High"
        }
    )

    data = response.get_json()

    assert response.status_code == 201
    assert data["title"] == "Test Jenkins Pipeline"
    assert data["priority"] == "High"
    assert data["completed"] is False


def test_create_task_without_title(client):
    response = client.post(
        "/api/tasks",
        json={
            "description": "Missing title test",
            "priority": "Medium"
        }
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Title is required"


def test_invalid_priority(client):
    response = client.post(
        "/api/tasks",
        json={
            "title": "Invalid Priority",
            "priority": "Critical"
        }
    )

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_update_task(client):
    create_response = client.post(
        "/api/tasks",
        json={
            "title": "Original Task",
            "priority": "Low"
        }
    )

    task_id = create_response.get_json()["id"]

    response = client.put(
        f"/api/tasks/{task_id}",
        json={
            "title": "Updated Task",
            "priority": "High",
            "completed": True
        }
    )

    data = response.get_json()

    assert response.status_code == 200
    assert data["title"] == "Updated Task"
    assert data["priority"] == "High"
    assert data["completed"] is True


def test_delete_task(client):
    create_response = client.post(
        "/api/tasks",
        json={
            "title": "Delete Me",
            "priority": "Medium"
        }
    )

    task_id = create_response.get_json()["id"]

    response = client.delete(f"/api/tasks/{task_id}")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Task deleted successfully"

    missing_response = client.get(f"/api/tasks/{task_id}")

    assert missing_response.status_code == 404
    assert missing_response.get_json()["error"] == "Resource not found"