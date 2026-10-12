import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

_base = os.path.abspath(os.path.dirname(__file__))


def is_production():
    """True when ENV or FLASK_ENV is set to 'production' (read at call time)."""
    return (
        os.getenv("FLASK_ENV", "").lower() == "production"
        or os.getenv("ENV", "").lower() == "production"
    )


def _int_env(name, default):
    try:
        return int(os.getenv(name, default))
    except (TypeError, ValueError):
        return default


_is_prod = is_production()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        if _is_prod:
            raise RuntimeError("SECRET_KEY must be set in production")
        SECRET_KEY = "dev-secret"

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    if not JWT_SECRET_KEY:
        if _is_prod:
            raise RuntimeError("JWT_SECRET_KEY must be set in production")
        JWT_SECRET_KEY = "dev-jwt-secret"

    _db = (os.getenv("DATABASE_URL") or "").strip()
    if not _db:
        _db = "sqlite:///" + os.path.join(_base, "..", "bigtree.db")
    if _db.startswith("postgres://"):
        _db = _db.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = _db
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=12)

    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    # AI guardrails (0 disables a rate limit)
    AI_TIMEOUT_SECONDS = _int_env("AI_TIMEOUT_SECONDS", 30)
    AI_MAX_OUTPUT_TOKENS = _int_env("AI_MAX_OUTPUT_TOKENS", 4096)
    AI_RATE_LIMIT_PER_MINUTE = _int_env("AI_RATE_LIMIT_PER_MINUTE", 10)
    AI_RATE_LIMIT_PER_DAY = _int_env("AI_RATE_LIMIT_PER_DAY", 200)
