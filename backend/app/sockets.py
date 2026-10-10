from flask import request
from flask_jwt_extended import decode_token
from flask_socketio import emit, join_room, leave_room

from app.extensions import db, socketio
from app.models import ChatMessage, ProjectMember

connected = {}  # socket id -> user id


def _room(project_id):
    return f"project_{project_id}"


def _is_member(user_id, project_id):
    return (
        ProjectMember.query.filter_by(project_id=project_id, user_id=user_id).first()
        is not None
    )


@socketio.on("connect")
def on_connect(auth=None):
    token = (auth or {}).get("token")
    try:
        user_id = int(decode_token(token)["sub"])
    except Exception:
        return False  # reject the connection
    connected[request.sid] = user_id


@socketio.on("disconnect")
def on_disconnect(*args):
    connected.pop(request.sid, None)


@socketio.on("join_project")
def on_join(data):
    user_id = connected.get(request.sid)
    try:
        project_id = int((data or {}).get("project_id"))
    except (TypeError, ValueError):
        emit("error", {"error": "project_id is required"})
        return
    if not user_id or not _is_member(user_id, project_id):
        emit("error", {"error": "Not a member of this project"})
        return
    join_room(_room(project_id))
    emit("joined", {"project_id": project_id})


@socketio.on("leave_project")
def on_leave(data):
    try:
        project_id = int((data or {}).get("project_id"))
    except (TypeError, ValueError):
        return
    leave_room(_room(project_id))


@socketio.on("send_message")
def on_send(data):
    user_id = connected.get(request.sid)
    data = data or {}
    try:
        project_id = int(data.get("project_id"))
    except (TypeError, ValueError):
        emit("error", {"error": "project_id is required"})
        return

    body = (data.get("body") or "").strip()
    if not body or len(body) > 2000:
        emit("error", {"error": "Message must be 1-2000 characters"})
        return
    if not user_id or not _is_member(user_id, project_id):
        emit("error", {"error": "Not a member of this project"})
        return

    message = ChatMessage(project_id=project_id, sender_id=user_id, body=body)
    db.session.add(message)
    db.session.commit()
    emit("new_message", message.to_dict(), room=_room(project_id))
