from datetime import timedelta

from flask import Blueprint, current_app, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import func

from app.extensions import db
from app.models import AIConversation, AIMessage, Persona
from app.schemas import AIChatSchema
from app.services.ai_service import build_project_context, generate
from app.utils import (
    ApiError,
    current_user_id,
    get_project_for_member,
    parse_body,
    utcnow,
)

ai_bp = Blueprint("ai", __name__)


def _enforce_rate_limit(uid):
    """Per-user limits counted from saved messages, so they hold across workers."""
    cfg = current_app.config
    windows = (
        (timedelta(minutes=1), cfg.get("AI_RATE_LIMIT_PER_MINUTE", 10), "a minute"),
        (timedelta(days=1), cfg.get("AI_RATE_LIMIT_PER_DAY", 200), "a day"),
    )
    now = utcnow()
    for window, limit, label in windows:
        if not limit:
            continue
        used = (
            db.session.query(func.count(AIMessage.id))
            .join(AIConversation, AIMessage.conversation_id == AIConversation.id)
            .filter(
                AIConversation.user_id == uid,
                AIMessage.role == "user",
                AIMessage.created_at >= now - window,
            )
            .scalar()
        )
        if used >= limit:
            raise ApiError(
                f"AI limit reached ({limit} messages {label}). Please try again later.",
                429,
            )


@ai_bp.post("/projects/<int:project_id>/ai/chat")
@jwt_required()
def chat(project_id):
    uid = current_user_id()
    project, _ = get_project_for_member(project_id, uid)
    data = parse_body(AIChatSchema())
    _enforce_rate_limit(uid)

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

    history = [(m.role, m.content) for m in conversation.messages] if conversation else []
    history.append(("user", data["message"]))

    # Call the model before writing anything, so no database transaction stays
    # open during the network call and failures leave no half-saved chat behind.
    result = generate(
        history,
        persona.system_prompt if persona else None,
        build_project_context(project),
    )
    if not result.ok:
        raise ApiError(result.text, 503)

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

    user_msg = AIMessage(
        conversation_id=conversation.id, role="user", content=data["message"]
    )
    ai_msg = AIMessage(
        conversation_id=conversation.id, role="assistant", content=result.text
    )
    db.session.add_all([user_msg, ai_msg])
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
    rows = (
        AIConversation.query.filter_by(project_id=project_id, user_id=uid)
        .order_by(AIConversation.id.desc())
        .all()
    )
    return jsonify([c.to_dict() for c in rows])


@ai_bp.get("/projects/<int:project_id>/ai/conversations/<int:conversation_id>/messages")
@jwt_required()
def list_messages(project_id, conversation_id):
    uid = current_user_id()
    get_project_for_member(project_id, uid)
    conversation = AIConversation.query.filter_by(
        id=conversation_id, project_id=project_id, user_id=uid
    ).first()
    if not conversation:
        raise ApiError("Conversation not found", 404)
    return jsonify([m.to_dict() for m in conversation.messages])
