import os

from flask import Flask, jsonify
from flask_cors import CORS

from app.config import Config
from app.extensions import db, migrate, jwt, socketio
from app.utils import ApiError


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.config["UPLOAD_FOLDER"] = os.path.abspath(app.config["UPLOAD_FOLDER"])
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    CORS(app, resources={r"/*": {"origins": "*"}})

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    from app import models  # noqa: F401  (registers models for migrations)
    from app.routes import register_blueprints
    from app import sockets  # noqa: F401  (registers socket handlers)
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
