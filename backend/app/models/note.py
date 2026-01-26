"""
Note and NoteEmbedding models for storing uploaded content and embeddings
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
    Float,
    LargeBinary,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Note(Base):
    """Note model - stores extracted text from uploaded files"""

    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(
        Integer, ForeignKey("reports.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # File information
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)  # pdf, txt, png, jpg, etc.
    file_size = Column(Integer, nullable=False)  # in bytes
    file_path = Column(String(500), nullable=False)  # S3 path

    # Extracted content
    content = Column(Text, nullable=False)  # Extracted text

    # Processing status
    status = Column(
        String(50), default="pending"
    )  # pending, processing, completed, failed
    processing_error = Column(Text, nullable=True)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    report = relationship("Report", back_populates="notes")
    user = relationship("User", back_populates="notes")
    embeddings = relationship(
        "NoteEmbedding", back_populates="note", cascade="all, delete-orphan"
    )


class NoteEmbedding(Base):
    """NoteEmbedding model - stores vector embeddings for semantic search"""

    __tablename__ = "note_embeddings"

    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(
        Integer, ForeignKey("notes.id", ondelete="CASCADE"), nullable=False
    )

    # Chunk information (for long texts, we split into chunks)
    chunk_index = Column(Integer, nullable=False)  # Which chunk this is (0, 1, 2, ...)
    chunk_text = Column(Text, nullable=False)  # The actual text chunk

    # Embedding vector stored as JSON text (compatible with SQLite and PostgreSQL)
    # Primary storage will be Qdrant, this is just for backup
    embedding_vector = Column(Text, nullable=True)  # JSON string of float array

    # Qdrant reference
    qdrant_id = Column(String(100), nullable=True)  # UUID in Qdrant

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    note = relationship("Note", back_populates="embeddings")
