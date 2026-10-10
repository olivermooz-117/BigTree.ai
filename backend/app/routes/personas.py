from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.models import Persona

personas_bp = Blueprint("personas", __name__)


@personas_bp.get("/personas")
@jwt_required()
def list_personas():
    personas = Persona.query.order_by(Persona.id).all()
    return jsonify([p.to_dict() for p in personas])
