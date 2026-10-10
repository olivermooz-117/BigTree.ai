from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import Task, ProjectMember
from app.schemas import TaskSchema
from app.utils import ApiError, parse_body, current_user_id, get_project_for_member

tasks_bp = Blueprint("tasks", __name__)


def _check_assignee(project_id, assignee_id):
    if assignee_id is None:
        return
    exists = ProjectMember.query.filter_by(
        project_id=project_id, user_id=assignee_id
    ).first()
    if not exists:
        raise ApiError("Assignee must be a project member", 400)


@tasks_bp.get("/projects/<int:project_id>/tasks")
@jwt_required()
def list_tasks(project_id):
    project, _ = get_project_for_member(project_id, current_user_id())
    tasks = sorted(project.tasks, key=lambda t: t.id)
    return jsonify([t.to_dict() for t in tasks])


@tasks_bp.post("/projects/<int:project_id>/tasks")
@jwt_required()
def create_task(project_id):
    get_project_for_member(project_id, current_user_id())
    data = parse_body(TaskSchema())
    _check_assignee(project_id, data.get("assignee_id"))
    task = Task(
        project_id=project_id,
        title=data["title"].strip(),
        status=data.get("status", "todo"),
        assignee_id=data.get("assignee_id"),
        due_date=data.get("due_date"),
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@tasks_bp.patch("/tasks/<int:task_id>")
@jwt_required()
def update_task(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        raise ApiError("Task not found", 404)
    get_project_for_member(task.project_id, current_user_id())

    data = parse_body(TaskSchema(), partial=True)
    if "assignee_id" in data:
        _check_assignee(task.project_id, data["assignee_id"])
        task.assignee_id = data["assignee_id"]
    if "title" in data:
        task.title = data["title"].strip()
    if "status" in data:
        task.status = data["status"]
    if "due_date" in data:
        task.due_date = data["due_date"]
    db.session.commit()
    return jsonify(task.to_dict())


@tasks_bp.delete("/tasks/<int:task_id>")
@jwt_required()
def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        raise ApiError("Task not found", 404)
    get_project_for_member(task.project_id, current_user_id())
    db.session.delete(task)
    db.session.commit()
    return "", 204
