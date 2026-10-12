from types import SimpleNamespace

import pytest

from app.production_checks import validate_production_config

GOOD = {
    "SECRET_KEY": "x9" * 20,
    "JWT_SECRET_KEY": "k7" * 20,
    "SQLALCHEMY_DATABASE_URI": "postgresql://user:pw@db.internal/bigtree",
    "CORS_ORIGINS": "https://app.bigtree.test",
    "GEMINI_API_KEY": "key",
}


def _check(monkeypatch, **overrides):
    monkeypatch.setenv("ENV", "production")
    monkeypatch.delenv("ALLOW_SQLITE_IN_PRODUCTION", raising=False)
    validate_production_config(SimpleNamespace(config={**GOOD, **overrides}))


def test_good_config_passes(monkeypatch):
    _check(monkeypatch)


def test_ignored_outside_production(monkeypatch):
    monkeypatch.delenv("ENV", raising=False)
    monkeypatch.delenv("FLASK_ENV", raising=False)
    validate_production_config(
        SimpleNamespace(config={"SECRET_KEY": "dev-secret", "CORS_ORIGINS": "*"})
    )


@pytest.mark.parametrize("bad", ["dev-secret-change-me", "short", "replace-with-a-long-random-secret-value"])
def test_weak_secret_rejected(monkeypatch, bad):
    with pytest.raises(RuntimeError, match="SECRET_KEY"):
        _check(monkeypatch, SECRET_KEY=bad)


def test_identical_secrets_rejected(monkeypatch):
    with pytest.raises(RuntimeError, match="must be different"):
        _check(monkeypatch, JWT_SECRET_KEY=GOOD["SECRET_KEY"])


def test_sqlite_rejected(monkeypatch):
    with pytest.raises(RuntimeError, match="DATABASE_URL"):
        _check(monkeypatch, SQLALCHEMY_DATABASE_URI="sqlite:///bigtree.db")


@pytest.mark.parametrize(
    "origins",
    ["", "*", "http://app.bigtree.test", "https://app.bigtree.test/"],
)
def test_bad_cors_rejected(monkeypatch, origins):
    with pytest.raises(RuntimeError, match="CORS"):
        _check(monkeypatch, CORS_ORIGINS=origins)
