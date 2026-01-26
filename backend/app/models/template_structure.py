"""
Template structure models for storing PDF template information
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship

from app.core.database import Base


class TemplateStructure(Base):
    """
    Model for storing extracted PDF template structure
    """

    __tablename__ = "template_structures"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(
        Integer,
        ForeignKey("reports.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    upload_job_id = Column(
        Integer, ForeignKey("upload_jobs.id", ondelete="SET NULL"), nullable=True
    )

    # File information
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    total_pages = Column(Integer, nullable=False, default=0)

    # Extracted content
    full_text = Column(Text, nullable=True)
    pdf_metadata = Column(
        "metadata", JSON, nullable=True
    )  # PDF metadata (author, title, etc.) - mapped to 'metadata' column in DB

    # Processing status
    status = Column(
        String(50), nullable=False, default="pending"
    )  # pending, processing, completed, failed
    error_message = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    processed_at = Column(DateTime, nullable=True)

    # Relationships
    report = relationship("Report", back_populates="template_structure")
    sections = relationship(
        "TemplateSection", back_populates="template", cascade="all, delete-orphan"
    )
    upload_job = relationship("UploadJob", foreign_keys=[upload_job_id])

    def __repr__(self):
        return f"<TemplateStructure(id={self.id}, report_id={self.report_id}, status={self.status})>"


class TemplateSection(Base):
    """
    Model for storing individual sections extracted from PDF template
    """

    __tablename__ = "template_sections"

    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(
        Integer,
        ForeignKey("template_structures.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Section hierarchy
    parent_id = Column(
        Integer,
        ForeignKey("template_sections.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    level = Column(
        Integer, nullable=False, default=1
    )  # Heading level (1=H1, 2=H2, etc.)
    order = Column(Integer, nullable=False, default=0)  # Order within parent

    # Section content
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=True)  # Text content under this section

    # Position in document
    page_number = Column(Integer, nullable=True)
    position_top = Column(Float, nullable=True)  # Y-coordinate on page

    # Formatting hints
    font_size = Column(Float, nullable=True)
    font_name = Column(String(100), nullable=True)
    is_bold = Column(Integer, nullable=False, default=0)  # SQLite doesn't have boolean

    # Metadata
    word_count = Column(Integer, nullable=False, default=0)
    section_metadata = Column(
        "metadata", JSON, nullable=True
    )  # Mapped to 'metadata' column in DB

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    template = relationship("TemplateStructure", back_populates="sections")
    parent = relationship("TemplateSection", remote_side=[id], backref="children")

    def __repr__(self):
        return (
            f"<TemplateSection(id={self.id}, title='{self.title}', level={self.level})>"
        )

    @property
    def full_path(self) -> str:
        """Get full hierarchical path of section"""
        if self.parent:
            return f"{self.parent.full_path} > {self.title}"
        return self.title

    def to_dict(self) -> dict:
        """Convert section to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "level": self.level,
            "order": self.order,
            "content": self.content,
            "page_number": self.page_number,
            "word_count": self.word_count,
            "children": (
                [child.to_dict() for child in self.children]
                if hasattr(self, "children")
                else []
            ),
        }
