"""
User model
"""

from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    """User model for authentication and authorization"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    reports = relationship(
        "Report", back_populates="user", cascade="all, delete-orphan"
    )
    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email}>"
