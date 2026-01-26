"""
Upload and UploadJob schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UploadJobResponse(BaseModel):
    """Upload job response"""

    id: int
    report_id: int
    filename: str
    file_type: str  # template, note
    file_format: str  # pdf, txt, png, jpg
    file_size: int
    status: str  # pending, uploading, processing, completed, failed
    progress: int  # 0-100
    error_message: Optional[str] = None
    note_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UploadStatusResponse(BaseModel):
    """Upload status response"""

    upload_id: int
    status: str
    progress: int
    message: Optional[str] = None
    note_id: Optional[int] = None


class FileUploadResponse(BaseModel):
    """File upload response"""

    upload_job_id: int
    filename: str
    file_size: int
    status: str
    message: str
