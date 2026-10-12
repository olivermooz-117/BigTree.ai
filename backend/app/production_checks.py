import logging
import os

from app.config import is_production

log = logging.getLogger(__name__)

MIN_SECRET_LENGTH = 32


def _truthy(name):
    return os.getenv(name, "").strip().lower() in ("1", "true", "yes")


def _weak_secret(value):
    if not value or len(value) < MIN_SECRET_LENGTH:
        return True
    low = value.lower()
    return (
        low.startswith(("dev-", "replace-with", "change"))
        or "change-me" in low
        or "changeme" in low
    )


def _origins(raw):
    items = raw if isinstance(raw, (list, tuple)) else str(raw or "").split(",")
    return [str(o).strip() for o in items if str(o).strip()]


def validate_production_config(app):
    """Refuse to start in production with unsafe settings. No-op elsewhere."""
    if not is_production():
        return

    cfg = app.config
    problems = []

    secret = cfg.get("SECRET_KEY")
    jwt_secret = cfg.get("JWT_SECRET_KEY")
    if _weak_secret(secret):
        problems.append(
            f"SECRET_KEY must be a unique random value of at least {MIN_SECRET_LENGTH} characters, not a placeholder."
        )
    if _weak_secret(jwt_secret):
        problems.append(
            f"JWT_SECRET_KEY must be a unique random value of at least {MIN_SECRET_LENGTH} characters, not a placeholder."
        )
    if secret and secret == jwt_secret:
        problems.append("SECRET_KEY and JWT_SECRET_KEY must be different.")

    uri = str(cfg.get("SQLALCHEMY_DATABASE_URI") or "")
    if uri.startswith("sqlite") and not _truthy("ALLOW_SQLITE_IN_PRODUCTION"):
        problems.append(
            "DATABASE_URL must point to a managed database such as PostgreSQL. "
            "SQLite files are lost on most hosts when the app redeploys."
        )

    origins = _origins(cfg.get("CORS_ORIGINS"))
    if not origins:
        problems.append("CORS_ORIGINS must list your deployed frontend origin(s).")
    for origin in origins:
        if origin == "*":
            problems.append('CORS_ORIGINS must not contain "*".')
        elif not origin.startswith("https://"):
            problems.append(f"CORS origin {origin!r} must start with https://.")
        elif origin.endswith("/"):
            problems.append(f"CORS origin {origin!r} must not end with a slash.")

    if problems:
        raise RuntimeError(
            "Unsafe production configuration:\n- " + "\n- ".join(problems)
        )

    if not cfg.get("GEMINI_API_KEY"):
        log.warning("GEMINI_API_KEY is not set; the AI co-pilot will be unavailable.")
