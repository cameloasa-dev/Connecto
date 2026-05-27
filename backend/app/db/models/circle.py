"""
SQLAlchemy ORM models for the Social App (SQLite compatible)
"""
from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey
from datetime import datetime

class Circle(Base):
    __tablename__ = "circles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)

    owner = relationship("User", back_populates="owned_circles")
    members = relationship("CircleMember", back_populates="circle")
    posts = relationship("Post", back_populates="circle")
