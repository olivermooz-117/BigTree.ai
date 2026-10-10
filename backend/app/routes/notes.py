from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import Note
from app.schemas import NoteSchema
from app.utils import ApiError, parse_body, current_user_id, get_project_for_member

notes_bp = Blueprint("notes", __name__)


def _get_editable_note(note_id, uid):
    note = db.session.get(Note, note_id)
    if not note:
        raise ApiError("Note not found", 404)
    project, member = get_project_for_member(note.project_id, uid)
    if note.author_id != uid and member.role != "owner":
        raise ApiError("You can only change your own notes", 403)
    return note


@notes_bp.get("/projects/<int:project_id>/notes")
@jwt_required()
def list_notes(project_id):
    project, _ = get_project_for_member(project_id, current_user_id())
    notes = sorted(project.notes, key=lambda n: n.updated_at, reverse=True)
    return jsonify([n.to_dict() for n in notes])


@notes_bp.post("/projects/<int:project_id>/notes")
@jwt_required()
def create_note(project_id):
    uid = current_user_id()
    get_project_for_member(project_id, uid)
    data = parse_body(NoteSchema())
    note = Note(
        project_id=project_id,
        author_id=uid,
        title=data["title"].strip(),
        body=data.get("body", ""),
    )
    db.session.add(note)
    db.session.commit()
    return jsonify(note.to_dict()), 201


@notes_bp.patch("/notes/<int:note_id>")
@jwt_required()
def update_note(note_id):
    note = _get_editable_note(note_id, current_user_id())
    data = parse_body(NoteSchema(), partial=True)
    if "title" in data:
        note.title = data["title"].strip()
    if "body" in data:
        note.body = data["body"]
    db.session.commit()
    return jsonify(note.to_dict())


@notes_bp.delete("/notes/<int:note_id>")
@jwt_required()
def delete_note(note_id):
    note = _get_editable_note(note_id, current_user_id())
    db.session.delete(note)
    db.session.commit()
    return "", 204
