import os
import uuid

from flask import Blueprint, current_app, jsonify, request, send_from_directory
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models import ProjectFile
from app.utils import ApiError, current_user_id, get_project_for_member

files_bp = Blueprint("files", __name__)

ALLOWED_EXTENSIONS = {
    "png", "jpg", "jpeg", "gif", "webp",
    "pdf", "txt", "md", "csv", "doc", "docx",
    "mp3", "wav", "mp4",
}


def _folder(project_id):
    return os.path.join(current_app.config["UPLOAD_FOLDER"], str(project_id))


@files_bp.get("/projects/<int:project_id>/files")
@jwt_required()
def list_files(project_id):
    project, _ = get_project_for_member(project_id, current_user_id())
    files = sorted(project.files, key=lambda f: f.created_at, reverse=True)
    return jsonify([f.to_dict() for f in files])


@files_bp.post("/projects/<int:project_id>/files")
@jwt_required()
def upload_file(project_id):
    uid = current_user_id()
    get_project_for_member(project_id, uid)

    upload = request.files.get("file")
    if not upload or not upload.filename:
        raise ApiError("No file provided (use form field 'file')", 400)

    ext = upload.filename.rsplit(".", 1)[-1].lower() if "." in upload.filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise ApiError(f"File type '.{ext}' is not allowed", 400)

    stored_name = f"{uuid.uuid4().hex}.{ext}"
    folder = _folder(project_id)
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, stored_name)
    upload.save(path)

    record = ProjectFile(
        project_id=project_id,
        uploader_id=uid,
        filename=secure_filename(upload.filename) or stored_name,
        stored_name=stored_name,
        mime_type=upload.mimetype,
        size=os.path.getsize(path),
    )
    db.session.add(record)
    db.session.commit()
    return jsonify(record.to_dict()), 201


@files_bp.get("/files/<int:file_id>/download")
@jwt_required()
def download_file(file_id):
    record = db.session.get(ProjectFile, file_id)
    if not record:
        raise ApiError("File not found", 404)
    get_project_for_member(record.project_id, current_user_id())
    return send_from_directory(
        _folder(record.project_id),
        record.stored_name,
        as_attachment=True,
        download_name=record.filename,
    )


@files_bp.delete("/files/<int:file_id>")
@jwt_required()
def delete_file(file_id):
    uid = current_user_id()
    record = db.session.get(ProjectFile, file_id)
    if not record:
        raise ApiError("File not found", 404)
    _, member = get_project_for_member(record.project_id, uid)
    if record.uploader_id != uid and member.role != "owner":
        raise ApiError("You can only delete your own files", 403)

    path = os.path.join(_folder(record.project_id), record.stored_name)
    if os.path.exists(path):
        os.remove(path)
    db.session.delete(record)
    db.session.commit()
    return "", 204
