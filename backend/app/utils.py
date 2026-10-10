from datetime import datetime, timezone

from flask import request
from flask_jwt_extended import get_jwt_identity
from marshmallow import ValidationError

from app.extensions import db


def utcnow():
    return datetime.now(timezone.utc)


class ApiError(Exception):
    def __init__(self, message, status=400, details=None):
        super().__init__(message)
        self.message = message
        self.status = status
        self.details = details


def current_user_id():
    return int(get_jwt_identity())


def parse_body(schema, partial=False):
    payload = request.get_json(silent=True) or {}
    try:
        return schema.load(payload, partial=partial)
    except ValidationError as err:
        raise ApiError("Validation failed", 422, err.messages)


def get_project_for_member(project_id, user_id, roles=None):
    from app.models import Project, ProjectMember

    project = db.session.get(Project, project_id)
    if not project:
        raise ApiError("Project not found", 404)
    member = ProjectMember.query.filter_by(
        project_id=project_id, user_id=user_id
    ).first()
    if not member:
        raise ApiError("You are not a member of this project", 403)
    if roles and member.role not in roles:
        raise ApiError("You do not have permission to do that", 403)
    return project, member
