from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import User
from app.schemas import RegisterSchema, LoginSchema
from app.utils import ApiError, parse_body, current_user_id

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    data = parse_body(RegisterSchema())
    email = data["email"].lower()
    if User.query.filter_by(email=email).first():
        raise ApiError("Email already registered", 409)

    user = User(name=data["name"].strip(), email=email)
    user.set_password(data["password"])
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ApiError("Email already registered", 409)

    token = create_access_token(identity=str(user.id))
    return jsonify(user=user.to_dict(), access_token=token), 201


@auth_bp.post("/login")
def login():
    data = parse_body(LoginSchema())
    user = User.query.filter_by(email=data["email"].lower()).first()
    if not user or not user.check_password(data["password"]):
        raise ApiError("Invalid email or password", 401)

    token = create_access_token(identity=str(user.id))
    return jsonify(user=user.to_dict(), access_token=token)


@auth_bp.get("/me")
@jwt_required()
def me():
    user = db.session.get(User, current_user_id())
    if not user:
        raise ApiError("User not found", 404)
    return jsonify(user.to_dict())
