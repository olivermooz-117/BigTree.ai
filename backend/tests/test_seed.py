from app.models import Persona, User


def test_seed_creates_personas_only(app):
    res = app.test_cli_runner().invoke(args=["seed"])
    assert res.exit_code == 0
    assert Persona.query.filter_by(name="Editor").first() is not None
    assert User.query.filter_by(email="demo@bigtree.ai").first() is None


def test_seed_demo_works_in_development(app, monkeypatch):
    monkeypatch.delenv("ENV", raising=False)
    monkeypatch.delenv("FLASK_ENV", raising=False)
    res = app.test_cli_runner().invoke(args=["seed-demo"])
    assert res.exit_code == 0
    user = User.query.filter_by(email="demo@bigtree.ai").first()
    assert user is not None
    assert user.check_password("Demo1234!")


def test_seed_demo_blocked_in_production(app, monkeypatch):
    monkeypatch.setenv("ENV", "production")
    monkeypatch.delenv("ALLOW_DEMO_SEED", raising=False)
    res = app.test_cli_runner().invoke(args=["seed-demo"])
    assert res.exit_code != 0
    assert User.query.filter_by(email="demo@bigtree.ai").first() is None


def test_seed_demo_in_production_needs_flag_and_password(app, monkeypatch):
    monkeypatch.setenv("ENV", "production")
    monkeypatch.setenv("ALLOW_DEMO_SEED", "true")
    monkeypatch.setenv("DEMO_PASSWORD", "short")
    assert app.test_cli_runner().invoke(args=["seed-demo"]).exit_code != 0

    monkeypatch.setenv("DEMO_PASSWORD", "a-long-demo-password-1")
    res = app.test_cli_runner().invoke(args=["seed-demo"])
    assert res.exit_code == 0
    user = User.query.filter_by(email="demo@bigtree.ai").first()
    assert user is not None and user.check_password("a-long-demo-password-1")
