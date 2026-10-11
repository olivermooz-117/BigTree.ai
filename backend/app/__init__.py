import os

from flask import Flask, jsonify
from flask_cors import CORS

from app.config import Config
from app.extensions import db, migrate, jwt, socketio
from app.utils import ApiError


def _allowed_origins(app):
    """Read explicit frontend origins; never enable wildcard CORS in production."""
    configured = app.config.get("CORS_ORIGINS", "")
    if isinstance(configured, (list, tuple)):
        origins = [str(origin).strip() for origin in configured if str(origin).strip()]
    else:
        origins = [origin.strip() for origin in str(configured).split(",") if origin.strip()]

    if not origins and not app.config.get("TESTING", False):
        # Local development only. Production should set CORS_ORIGINS explicitly.
        is_production = (
            os.getenv("FLASK_ENV", "").lower() == "production"
            or os.getenv("ENV", "").lower() == "production"
        )
        if is_production:
            raise RuntimeError("CORS_ORIGINS must be set in production")
        origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

    return origins


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.config["UPLOAD_FOLDER"] = os.path.abspath(app.config["UPLOAD_FOLDER"])
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    origins = _allowed_origins(app)
    CORS(app, resources={r"/*": {"origins": origins}})
    socketio.init_app(app, cors_allowed_origins=origins)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    @jwt.unauthorized_loader
    def _unauthorized(reason):
        return jsonify(error="Missing or invalid token", detail=reason), 401

    @jwt.invalid_token_loader
    def _invalid(reason):
        return jsonify(error="Invalid token", detail=reason), 401

    @jwt.expired_token_loader
    def _expired(jwt_header, jwt_payload):
        return jsonify(error="Token has expired"), 401

    from app import models  # noqa: F401
    from app.routes import register_blueprints
    from app import sockets  # noqa: F401
    from app.seed import register_cli

    register_blueprints(app)
    register_cli(app)

    @app.errorhandler(ApiError)
    def handle_api_error(err):
        body = {"error": err.message}
        if err.details:
            body["details"] = err.details
        return jsonify(body), err.status

    @app.errorhandler(404)
    def handle_404(_):
        return jsonify(error="Not found"), 404

    @app.errorhandler(413)
    def handle_413(_):
        return jsonify(error="File too large (max 10 MB)"), 413

    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "app": "Bigtree.ai"})

    return app
