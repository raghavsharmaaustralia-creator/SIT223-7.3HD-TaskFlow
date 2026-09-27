from flask import Blueprint, jsonify, request
from app import db
from app.models import Task

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return jsonify({
        "application": "TaskFlow",
        "status": "running",
        "message": "TaskFlow API is ready"
    })


@main.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "TaskFlow"
    }), 200


@main.route("/api/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return jsonify([task.to_dict() for task in tasks])


@main.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True) or {}

    title = str(data.get("title", "")).strip()
    description = str(data.get("description", "")).strip()
    priority = str(data.get("priority", "Medium")).strip().capitalize()

    if not title:
        return jsonify({
            "error": "Title is required"
        }), 400

    if priority not in {"Low", "Medium", "High"}:
        return jsonify({
            "error": "Priority must be Low, Medium or High"
        }), 400

    task = Task(
        title=title,
        description=description,
        priority=priority
    )

    db.session.add(task)
    db.session.commit()

    return jsonify(task.to_dict()), 201


@main.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = db.get_or_404(Task, task_id)
    return jsonify(task.to_dict())


@main.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = db.get_or_404(Task, task_id)
    data = request.get_json(silent=True) or {}

    if "title" in data:
        title = str(data["title"]).strip()

        if not title:
            return jsonify({
                "error": "Title cannot be empty"
            }), 400

        task.title = title

    if "description" in data:
        task.description = str(data["description"]).strip()

    if "priority" in data:
        priority = str(data["priority"]).strip().capitalize()

        if priority not in {"Low", "Medium", "High"}:
            return jsonify({
                "error": "Priority must be Low, Medium or High"
            }), 400

        task.priority = priority

    if "completed" in data:
        if not isinstance(data["completed"], bool):
            return jsonify({
                "error": "Completed must be true or false"
            }), 400

        task.completed = data["completed"]

    db.session.commit()

    return jsonify(task.to_dict())


@main.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = db.get_or_404(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({
        "message": "Task deleted successfully"
    }), 200


@main.app_errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Resource not found"
    }), 404