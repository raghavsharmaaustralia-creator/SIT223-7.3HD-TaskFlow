from app import create_app, db


def test_task_lifecycle_integration():
    """
    Integration test:
    verifies the complete TaskFlow task lifecycle through the API
    and database: create -> retrieve -> update -> delete.
    """

    app = create_app()

    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:"
    )

    with app.app_context():
        db.create_all()

        client = app.test_client()

        # CREATE
        create_response = client.post(
            "/api/tasks",
            json={
                "title": "Integration Test Task",
                "description": "Testing complete task lifecycle",
                "priority": "High"
            }
        )

        assert create_response.status_code == 201
        task = create_response.get_json()
        task_id = task["id"]

        # READ
        get_response = client.get(f"/api/tasks/{task_id}")

        assert get_response.status_code == 200
        assert get_response.get_json()["title"] == "Integration Test Task"

        # UPDATE
        update_response = client.put(
            f"/api/tasks/{task_id}",
            json={
                "completed": True
            }
        )

        assert update_response.status_code == 200
        assert update_response.get_json()["completed"] is True

        # DELETE
        delete_response = client.delete(f"/api/tasks/{task_id}")

        assert delete_response.status_code == 200

        # VERIFY DELETION
        missing_response = client.get(f"/api/tasks/{task_id}")

        assert missing_response.status_code == 404

        db.session.remove()
        db.drop_all()