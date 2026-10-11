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
    "pdf", "txt", "md", "csv", "json",
    "doc", "docx", "xls", "xlsx",
}


def _allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@files_bp.get("/projects/<int:project_id>/files")
@jwt_required()
def list_files(project_id):
    project, _ = get_project_for_member(project_id, current_user_id())
    return jsonify([f.to_dict() for f in project.files])


@files_bp.post("/projects/<int:project_id>/files")
@jwt_required()
def upload_file(project_id):
    uid = current_user_id()
    get_project_for_member(project_id, uid)

    if "file" not in request.files:
        raise ApiError("No file part", 400)
    file = request.files["file"]
    if not file or not file.filename:
        raise ApiError("No selected file", 400)
    if not _allowed(file.filename):
        raise ApiError("File type not allowed", 400)

    original = secure_filename(file.filename)
    ext = original.rsplit(".", 1)[1].lower()
    stored = f"{uuid.uuid4().hex}.{ext}"
    folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, stored)
    file.save(path)
    size = os.path.getsize(path)

    record = ProjectFile(
        project_id=project_id,
        uploader_id=uid,
        filename=original,
        url=stored,
        mime_type=file.mimetype or "application/octet-stream",
        size=size,
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
    folder = current_app.config["UPLOAD_FOLDER"]
    return send_from_directory(
        folder,
        record.url,
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
    project, member = get_project_for_member(record.project_id, uid)
    if record.uploader_id != uid and member.role != "owner":
        raise ApiError("You can only delete your own files", 403)

    path = os.path.join(current_app.config["UPLOAD_FOLDER"], record.url)
    if os.path.isfile(path):
        os.remove(path)
    db.session.delete(record)
    db.session.commit()
    return jsonify(ok=True)
