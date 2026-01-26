"""
UploadJob model for tracking file upload and processing jobs
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class UploadJob(Base):
    """UploadJob model - tracks async file upload and processing jobs"""

    __tablename__ = "upload_jobs"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(
        Integer, ForeignKey("reports.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # File information
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)  # template, note
    file_format = Column(String(50), nullable=False)  # pdf, txt, png, jpg, etc.
    file_size = Column(Integer, nullable=False)  # in bytes
    file_path = Column(String(500), nullable=True)  # S3 path (set after upload)

    # Job status
    status = Column(
        String(50), default="pending"
    )  # pending, uploading, processing, completed, failed
    progress = Column(Integer, default=0)  # 0-100 percentage

    # Processing details
    celery_task_id = Column(String(255), nullable=True)  # Celery task ID
    error_message = Column(Text, nullable=True)
    processing_details = Column(Text, nullable=True)  # JSON string with details

    # Result references
    note_id = Column(
        Integer, ForeignKey("notes.id", ondelete="SET NULL"), nullable=True
    )  # If this created a note
    template_structure_id = Column(Integer, nullable=True)  # If this created a template

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    report = relationship("Report")
    user = relationship("User")
    note = relationship("Note", foreign_keys=[note_id])

    def __repr__(self):
        return f"<UploadJob {self.id} - {self.filename} ({self.status})>"
