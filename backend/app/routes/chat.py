from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.models import ChatMessage
from app.utils import current_user_id, get_project_for_member

chat_bp = Blueprint("chat", __name__)


@chat_bp.get("/projects/<int:project_id>/messages")
@jwt_required()
def list_messages(project_id):
    get_project_for_member(project_id, current_user_id())

    limit = min(request.args.get("limit", 50, type=int), 200)
    before = request.args.get("before", type=int)

    query = ChatMessage.query.filter_by(project_id=project_id)
    if before:
        query = query.filter(ChatMessage.id < before)
    messages = query.order_by(ChatMessage.id.desc()).limit(limit).all()
    messages.reverse()
    return jsonify([m.to_dict() for m in messages])
