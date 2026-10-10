from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import AIConversation, AIMessage, Persona
from app.schemas import AIChatSchema
from app.services.ai_service import build_project_context, generate_reply
from app.utils import ApiError, parse_body, current_user_id, get_project_for_member

ai_bp = Blueprint("ai", __name__)


@ai_bp.post("/projects/<int:project_id>/ai/chat")
@jwt_required()
def chat(project_id):
    uid = current_user_id()
    project, _ = get_project_for_member(project_id, uid)
    data = parse_body(AIChatSchema())

    conversation = None
    if data.get("conversation_id"):
        conversation = AIConversation.query.filter_by(
            id=data["conversation_id"], project_id=project_id, user_id=uid
        ).first()
        if not conversation:
            raise ApiError("Conversation not found", 404)

    persona_id = data.get("persona_id") or (
        conversation.persona_id if conversation else None
    )
    if persona_id:
        persona = db.session.get(Persona, persona_id)
        if not persona:
            raise ApiError("Persona not found", 404)
    else:
        persona = Persona.query.filter_by(is_default=True).first()

    if not conversation:
        conversation = AIConversation(
            project_id=project_id,
            user_id=uid,
            persona_id=persona.id if persona else None,
            title=data["message"][:60],
        )
        db.session.add(conversation)
        db.session.flush()
    elif persona and conversation.persona_id != persona.id:
        conversation.persona_id = persona.id

    history = [(m.role, m.content) for m in conversation.messages]
    history.append(("user", data["message"]))

    user_msg = AIMessage(
        conversation_id=conversation.id, role="user", content=data["message"]
    )
    db.session.add(user_msg)

    reply_text = generate_reply(
        history,
        persona.system_prompt if persona else None,
        build_project_context(project),
    )
    ai_msg = AIMessage(
        conversation_id=conversation.id, role="assistant", content=reply_text
    )
    db.session.add(ai_msg)
    db.session.commit()

    return jsonify(
        conversation=conversation.to_dict(),
        user_message=user_msg.to_dict(),
        reply=ai_msg.to_dict(),
    )


@ai_bp.get("/projects/<int:project_id>/ai/conversations")
@jwt_required()
def list_conversations(project_id):
    uid = current_user_id()
    get_project_for_member(project_id, uid)
    conversations = (
        AIConversation.query.filter_by(project_id=project_id, user_id=uid)
        .order_by(AIConversation.id.desc())
        .all()
    )
    return jsonify([c.to_dict() for c in conversations])


@ai_bp.get("/ai/conversations/<int:conversation_id>/messages")
@jwt_required()
def conversation_messages(conversation_id):
    uid = current_user_id()
    conversation = db.session.get(AIConversation, conversation_id)
    if not conversation or conversation.user_id != uid:
        raise ApiError("Conversation not found", 404)
    return jsonify([m.to_dict() for m in conversation.messages])


@ai_bp.delete("/ai/conversations/<int:conversation_id>")
@jwt_required()
def delete_conversation(conversation_id):
    uid = current_user_id()
    conversation = db.session.get(AIConversation, conversation_id)
    if not conversation or conversation.user_id != uid:
        raise ApiError("Conversation not found", 404)
    db.session.delete(conversation)
    db.session.commit()
    return "", 204
