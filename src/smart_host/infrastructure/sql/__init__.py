from __future__ import annotations

"""SQLAlchemy database setup and initialization."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite:///smart_host.db"

engine = create_engine(
    DATABASE_URL,
    future=True,
)

SessionLocal = sessionmaker(bind=engine, future=True)


class Base(DeclarativeBase):
    """Base declarative class."""


def init_db() -> None:
    """Create database tables if they do not exist."""
    from . import models  # noqa: F401 -- import models for metadata

    Base.metadata.create_all(engine, checkfirst=True)
