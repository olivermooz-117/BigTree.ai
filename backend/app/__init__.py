import os
from flask import Flask, jsonify
from flask_cors import CORS

from app.config import Config
from app.extensions import db, migrate, jwt, socketio


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    CORS(app, resources={r"/*": {"origins": "*"}})

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    # Models and blueprints get registered here as we build them
    # from app import models
    # from app.routes.auth import auth_bp
    # app.register_blueprint(auth_bp, url_prefix="/auth")

    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "app": "Bigtree.ai"})

    return app
