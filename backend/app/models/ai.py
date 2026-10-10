from app.extensions import db
from app.utils import utcnow


class Persona(db.Model):
    __tablename__ = "personas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255), default="")
    system_prompt = db.Column(db.Text, nullable=False)
    is_default = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_default": self.is_default,
        }


class AIConversation(db.Model):
    __tablename__ = "ai_conversations"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(
        db.Integer,
        db.ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    persona_id = db.Column(db.Integer, db.ForeignKey("personas.id"))
    title = db.Column(db.String(120), default="New conversation")
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)

    persona = db.relationship("Persona")
    messages = db.relationship(
        "AIMessage",
        backref="conversation",
        cascade="all, delete-orphan",
        order_by="AIMessage.id",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "persona_id": self.persona_id,
            "title": self.title,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class AIMessage(db.Model):
    __tablename__ = "ai_messages"

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(
        db.Integer,
        db.ForeignKey("ai_conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role = db.Column(db.String(20), nullable=False)  # "user" or "assistant"
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "role": self.role,
            "content": self.content,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
