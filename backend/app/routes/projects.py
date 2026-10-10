import os
import shutil

from flask import Blueprint, current_app, jsonify
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import Project, ProjectMember, User
from app.schemas import ProjectSchema, MemberSchema
from app.utils import ApiError, parse_body, current_user_id, get_project_for_member

projects_bp = Blueprint("projects", __name__)


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
    return jsonify([{**p.to_dict(), "role": role} for p, role in rows])


@projects_bp.post("/projects")
@jwt_required()
def create_project():
    uid = current_user_id()
    data = parse_body(ProjectSchema())
    project = Project(
        title=data["title"].strip(),
        description=data.get("description", ""),
        owner_id=uid,
    )
    project.members.append(ProjectMember(user_id=uid, role="owner"))
    db.session.add(project)
    db.session.commit()
    return jsonify({**project.to_dict(), "role": "owner"}), 201


@projects_bp.get("/projects/<int:project_id>")
@jwt_required()
def get_project(project_id):
    project, member = get_project_for_member(project_id, current_user_id())
    return jsonify(
        {
            **project.to_dict(),
            "role": member.role,
            "members": [m.to_dict() for m in project.members],
        }
    )


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
        project.description = data["description"]
    db.session.commit()
    return jsonify(project.to_dict())


@projects_bp.delete("/projects/<int:project_id>")
@jwt_required()
def delete_project(project_id):
    project, _ = get_project_for_member(
        project_id, current_user_id(), roles=["owner"]
    )
    folder = os.path.join(current_app.config["UPLOAD_FOLDER"], str(project.id))
    shutil.rmtree(folder, ignore_errors=True)
    db.session.delete(project)
    db.session.commit()
    return "", 204


@projects_bp.get("/projects/<int:project_id>/members")
@jwt_required()
def list_members(project_id):
    project, _ = get_project_for_member(project_id, current_user_id())
    return jsonify([m.to_dict() for m in project.members])


@projects_bp.post("/projects/<int:project_id>/members")
@jwt_required()
def add_member(project_id):
    project, _ = get_project_for_member(
        project_id, current_user_id(), roles=["owner"]
    )
    data = parse_body(MemberSchema())
    user = User.query.filter_by(email=data["email"].lower()).first()
    if not user:
        raise ApiError("No user with that email", 404)
    if ProjectMember.query.filter_by(project_id=project.id, user_id=user.id).first():
        raise ApiError("User is already a member", 409)

    member = ProjectMember(project_id=project.id, user_id=user.id, role="member")
    db.session.add(member)
    db.session.commit()
    return jsonify(member.to_dict()), 201


@projects_bp.delete("/projects/<int:project_id>/members/<int:user_id>")
@jwt_required()
def remove_member(project_id, user_id):
    project, _ = get_project_for_member(
        project_id, current_user_id(), roles=["owner"]
    )
    if user_id == project.owner_id:
        raise ApiError("The owner cannot be removed", 400)
    member = ProjectMember.query.filter_by(
        project_id=project.id, user_id=user_id
    ).first()
    if not member:
        raise ApiError("Member not found", 404)
    db.session.delete(member)
    db.session.commit()
    return "", 204
