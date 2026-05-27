"""
SQLAlchemy ORM models for the Social App (SQLite compatible)
"""
from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey
from datetime import datetime

class CircleMember(Base):
    __tablename__ = "circle_members"

    circle_id: Mapped[int] = mapped_column(ForeignKey("circles.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    role: Mapped[str] = mapped_column(String(20), default="member")
    joined_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)

    circle = relationship("Circle", back_populates="members")
    user = relationship("User", back_populates="circle_memberships")
