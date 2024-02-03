"""
Configuration for LedgerLite.

Production / intended usage: PostgreSQL, configured via the DATABASE_URL
environment variable, e.g.

    postgresql+psycopg2://ledgeruser:ledgerpass@localhost:5432/ledgerlite

Local dev / testing fallback: if DATABASE_URL is not set, LedgerLite falls
back to a local SQLite file (instance/ledgerlite.db). This fallback exists
purely so the app's logic (auth, expenses, budgets, roast generation) can be
exercised without a running PostgreSQL server. It is NOT the intended
production database.
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))


def _normalize_db_url(url: str) -> str:
    # Heroku-style postgres:// URLs need to be rewritten for SQLAlchemy 1.4+/psycopg2
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me-in-production")

    _database_url = os.environ.get("DATABASE_URL")
    if _database_url:
        SQLALCHEMY_DATABASE_URI = _normalize_db_url(_database_url)
        USING_SQLITE_FALLBACK = False
    else:
        instance_dir = os.path.join(basedir, "instance")
        os.makedirs(instance_dir, exist_ok=True)
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(instance_dir, "ledgerlite.db")
        USING_SQLITE_FALLBACK = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False
