"""
Report and ReportSection schemas
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# Report Schemas
class ReportBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class ReportCreate(ReportBase):
    pass


class ReportUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[str] = None


class ReportSectionResponse(BaseModel):
    id: int
    report_id: int
    title: str
    content: str
    order: int
    word_count: int
    is_completed: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class ReportResponse(ReportBase):
    id: int
    user_id: int
    status: str
    progress_percentage: float
    total_word_count: int
    created_at: datetime
    updated_at: Optional[datetime]
    sections: List[ReportSectionResponse] = []

    class Config:
        from_attributes = True


class ReportListResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    progress_percentage: float
    total_word_count: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# ReportSection Schemas
class ReportSectionBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = ""
    order: int


class ReportSectionCreate(ReportSectionBase):
    report_id: int


class ReportSectionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = None
    order: Optional[int] = None
    is_completed: Optional[bool] = None
