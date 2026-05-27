"""
SQLAlchemy ORM models for the Social App (SQLite compatible)
"""
from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey
from datetime import datetime

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    circle_id: Mapped[int | None] = mapped_column(ForeignKey("circles.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(), onupdate=datetime.utcnow)

    author = relationship("User", back_populates="posts")
    circle = relationship("Circle", back_populates="posts")
