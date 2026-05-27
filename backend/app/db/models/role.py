"""
SQLAlchemy ORM models for the Social App (SQLite compatible)
"""
from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))
