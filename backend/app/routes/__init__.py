from app.routes.auth import auth_bp
from app.routes.projects import projects_bp
from app.routes.notes import notes_bp
from app.routes.files import files_bp
from app.routes.personas import personas_bp
from app.routes.ai import ai_bp
from app.routes.chat import chat_bp
from app.routes.tasks import tasks_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix="/auth")
    for bp in (
        projects_bp,
        notes_bp,
        files_bp,
        personas_bp,
        ai_bp,
        chat_bp,
        tasks_bp,
    ):
        app.register_blueprint(bp)
