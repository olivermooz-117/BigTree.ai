import os
import pytest

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "test-secret"
os.environ["JWT_SECRET_KEY"] = "test-jwt-secret"
os.environ.pop("GEMINI_API_KEY", None)

from app import create_app
from app.extensions import db
from app.models import User, Persona


@pytest.fixture()
def app():
    application = create_app()
    application.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )
    with application.app_context():
        db.create_all()
        if not Persona.query.filter_by(is_default=True).first():
            db.session.add(
                Persona(
                    name="Assistant",
                    description="Default",
                    system_prompt="You are a helpful assistant.",
                    is_default=True,
                )
            )
            db.session.commit()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def auth_headers(client):
    res = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
        },
    )
    assert res.status_code == 201
    token = res.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def second_user_headers(client):
    res = client.post(
        "/auth/register",
        json={
            "name": "Other User",
            "email": "other@example.com",
            "password": "password123",
        },
    )
    assert res.status_code == 201
    token = res.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
