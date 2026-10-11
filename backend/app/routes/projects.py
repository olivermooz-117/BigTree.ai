from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import Project, ProjectMember, User
from app.schemas import ProjectSchema, MemberSchema
from app.utils import ApiError, parse_body, current_user_id, get_project_for_member

projects_bp = Blueprint("projects", __name__)


def _project_payload(project, role=None):
    data = project.to_dict()
    data["members"] = [m.to_dict() for m in project.members]
    if role is not None:
        data["role"] = role
    return data


@projects_bp.get("/projects")
@jwt_required()
def list_projects():
    uid = current_user_id()
    rows = (
        db.session.query(Project, ProjectMember.role)
        .join(ProjectMember, ProjectMember.project_id == Project.id)
        .filter(ProjectMember.user_id == uid)
        .order_by(Project.updated_at.desc())
        .all()
    )
    return jsonify([_project_payload(p, role) for p, role in rows])


@projects_bp.post("/projects")
@jwt_required()
def create_project():
    uid = current_user_id()
    data = parse_body(ProjectSchema())
    project = Project(
        title=data["title"].strip(),
        description=data.get("description") or "",
        owner_id=uid,
    )
    project.members.append(ProjectMember(user_id=uid, role="owner"))
    db.session.add(project)
    db.session.commit()
    return jsonify(_project_payload(project, "owner")), 201


@projects_bp.get("/projects/<int:project_id>")
@jwt_required()
def get_project(project_id):
    project, member = get_project_for_member(project_id, current_user_id())
    return jsonify(_project_payload(project, member.role))


@projects_bp.patch("/projects/<int:project_id>")
@jwt_required()
def update_project(project_id):
    project, _ = get_project_for_member(
        project_id, current_user_id(), roles=["owner"]
    )
    data = parse_body(ProjectSchema(), partial=True)
    if "title" in data:
        project.title = data["title"].strip()
    if "description" in data:
        project.description = data["description"] or ""
    db.session.commit()
    return jsonify(_project_payload(project))


@projects_bp.delete("/projects/<int:project_id>")
@jwt_required()
def delete_project(project_id):
    project, _ = get_project_for_member(
        project_id, current_user_id(), roles=["owner"]
    )
    db.session.delete(project)
    db.session.commit()
    return jsonify(ok=True)


@projects_bp.post("/projects/<int:project_id>/members")
@jwt_required()
def add_member(project_id):
    get_project_for_member(project_id, current_user_id(), roles=["owner"])
    data = parse_body(MemberSchema())
    user = User.query.filter_by(email=data["email"].lower()).first()
    if not user:
        raise ApiError("User not found with that email", 404)
    existing = ProjectMember.query.filter_by(
        project_id=project_id, user_id=user.id
    ).first()
    if existing:
        raise ApiError("User is already a member", 409)
    member = ProjectMember(
        project_id=project_id,
        user_id=user.id,
        role=data.get("role") or "member",
    )
    db.session.add(member)
    db.session.commit()
    return jsonify(member.to_dict()), 201
