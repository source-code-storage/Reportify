"""
Note schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    filename: str
    file_type: str
    content: str


class NoteCreate(NoteBase):
    report_id: int
    file_size: int
    file_path: str


class NoteUpdate(BaseModel):
    content: Optional[str] = None
    status: Optional[str] = None
    processing_error: Optional[str] = None


class NoteResponse(BaseModel):
    id: int
    report_id: int
    user_id: int
    filename: str
    file_type: str
    file_size: int
    file_path: str
    content: str
    status: str
    processing_error: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class NoteListResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    file_size: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
