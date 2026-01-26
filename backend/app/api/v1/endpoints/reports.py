"""
Report management endpoints
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.report import Report, ReportSection
from app.schemas.report import (
    ReportCreate,
    ReportUpdate,
    ReportResponse,
    ReportListResponse,
    ReportSectionUpdate,
    ReportSectionResponse,
)
from app.services.report_service import ReportService

router = APIRouter()


@router.post("/", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def create_report(
    report_data: ReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new report"""
    report = ReportService.create_report(db, current_user.id, report_data)
    return report


@router.get("/", response_model=List[ReportListResponse])
def list_reports(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all reports for the current user"""
    reports = ReportService.get_user_reports(db, current_user.id, skip, limit)
    return reports


@router.get("/{report_id}", response_model=ReportResponse)
def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific report by ID"""
    report = ReportService.get_report(db, report_id, current_user.id)
    return report


@router.put("/{report_id}", response_model=ReportResponse)
def update_report(
    report_id: int,
    report_data: ReportUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a report"""
    report = ReportService.update_report(db, report_id, current_user.id, report_data)
    return report


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a report"""
    ReportService.delete_report(db, report_id, current_user.id)
    return None


@router.get("/{report_id}/sections", response_model=List[ReportSectionResponse])
def get_sections(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all sections for a report"""
    sections = ReportService.get_report_sections(db, report_id, current_user.id)
    return sections


@router.post(
    "/{report_id}/sections",
    response_model=ReportSectionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_section(
    report_id: int,
    title: str,
    order: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new section in a report"""
    section = ReportService.create_section(db, report_id, current_user.id, title, order)
    return section


@router.put("/{report_id}/sections/{section_id}", response_model=ReportSectionResponse)
def update_section(
    report_id: int,
    section_id: int,
    section_data: ReportSectionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a report section"""
    section = ReportService.update_section(
        db,
        report_id,
        section_id,
        current_user.id,
        title=section_data.title,
        content=section_data.content,
        order=section_data.order,
        is_completed=section_data.is_completed,
    )
    return section
