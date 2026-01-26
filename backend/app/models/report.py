"""
Report and ReportSection models
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
    Boolean,
    Float,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Report(Base):
    """Report model - represents a user's report project"""

    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="draft")  # draft, in_progress, completed
    progress_percentage = Column(Float, default=0.0)
    total_word_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="reports")
    sections = relationship(
        "ReportSection", back_populates="report", cascade="all, delete-orphan"
    )
    notes = relationship("Note", back_populates="report", cascade="all, delete-orphan")
    template_structure = relationship(
        "TemplateStructure",
        back_populates="report",
        uselist=False,
        cascade="all, delete-orphan",
    )


class ReportSection(Base):
    """ReportSection model - represents a section within a report"""

    __tablename__ = "report_sections"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(
        Integer, ForeignKey("reports.id", ondelete="CASCADE"), nullable=False
    )
    title = Column(String(255), nullable=False)
    content = Column(Text, default="")
    order = Column(Integer, nullable=False)  # Section order in the report
    word_count = Column(Integer, default=0)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    report = relationship("Report", back_populates="sections")
