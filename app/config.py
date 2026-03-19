from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def _build_db_uri() -> str:
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        return database_url.replace("postgres://", "postgresql://", 1)

    host = os.environ.get("SUPABASE_DB_HOST")
    port = os.environ.get("SUPABASE_DB_PORT", "5432")
    name = os.environ.get("SUPABASE_DB_NAME")
    user = os.environ.get("SUPABASE_DB_USER")
    password = os.environ.get("SUPABASE_DB_PASSWORD")
    if all([host, port, name, user, password]):
        return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{name}"

    return f"sqlite:///{BASE_DIR / 'data' / 'app.db'}"


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
    SQLALCHEMY_DATABASE_URI = _build_db_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    MAX_CONTENT_LENGTH = 1024 * 1024  # 1MB request cap
    WTF_CSRF_TIME_LIMIT = None
    RATELIMIT_DEFAULT = "120 per hour"
    RATELIMIT_STORAGE_URI = os.environ.get("RATELIMIT_STORAGE_URI", "memory://")
    TALISMAN_FORCE_HTTPS = os.environ.get("TALISMAN_FORCE_HTTPS", "false").lower() == "true"
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "")


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    TALISMAN_FORCE_HTTPS = False
    RATELIMIT_ENABLED = False


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False


CONFIG_BY_NAME = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
