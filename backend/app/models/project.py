from app.extensions import db
from app.utils import utcnow


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default="")
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    owner = db.relationship("User")
    members = db.relationship(
        "ProjectMember", backref="project", cascade="all, delete-orphan"
    )
    notes = db.relationship("Note", backref="project", cascade="all, delete-orphan")
    files = db.relationship(
        "ProjectFile", backref="project", cascade="all, delete-orphan"
    )
    tasks = db.relationship("Task", backref="project", cascade="all, delete-orphan")
    chat_messages = db.relationship(
        "ChatMessage", backref="project", cascade="all, delete-orphan"
    )
    ai_conversations = db.relationship(
        "AIConversation", backref="project", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "owner_id": self.owner_id,
            "member_count": len(self.members),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class ProjectMember(db.Model):
    __tablename__ = "project_members"
    __table_args__ = (
        db.UniqueConstraint("project_id", "user_id", name="uq_project_user"),
    )

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(
        db.Integer, db.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="member")
    joined_at = db.Column(db.DateTime(timezone=True), default=utcnow)

    user = db.relationship("User")

    def to_dict(self):
        return {
            "user": self.user.to_dict(),
            "role": self.role,
            "joined_at": self.joined_at.isoformat() if self.joined_at else None,
        }
