"""
Export endpoints for generating PDF and DOCX files
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import io

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.report import Report, ReportSection
from app.services.export_service import export_service

router = APIRouter()


class ExportRequest(BaseModel):
    """Request model for export"""

    report_id: int
    format: str = "pdf"  # pdf or docx


@router.post("/pdf")
async def export_to_pdf(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Export report to PDF format.

    Args:
        report_id: ID of the report to export
        db: Database session
        current_user: Current authenticated user

    Returns:
        PDF file as streaming response
    """
    # Get report
    report = (
        db.query(Report)
        .filter(Report.id == report_id, Report.user_id == current_user.id)
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Report not found"
        )

    # Get sections
    sections = (
        db.query(ReportSection)
        .filter(ReportSection.report_id == report_id)
        .order_by(ReportSection.order)
        .all()
    )

    # Convert sections to dict format
    sections_data = [
        {"title": section.title, "content": section.content or ""}
        for section in sections
    ]

    try:
        # Generate PDF
        pdf_bytes = export_service.export_to_pdf(
            report_title=report.title,
            sections=sections_data,
            author=current_user.name or current_user.email,
            metadata={"description": report.description},
        )

        # Generate filename
        filename = export_service.get_export_filename(report.title, "pdf")

        # Return as streaming response
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )

    except ImportError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate PDF: {str(e)}",
        )


@router.post("/docx")
async def export_to_docx(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Export report to DOCX format.

    Args:
        report_id: ID of the report to export
        db: Database session
        current_user: Current authenticated user

    Returns:
        DOCX file as streaming response
    """
    # Get report
    report = (
        db.query(Report)
        .filter(Report.id == report_id, Report.user_id == current_user.id)
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Report not found"
        )

    # Get sections
    sections = (
        db.query(ReportSection)
        .filter(ReportSection.report_id == report_id)
        .order_by(ReportSection.order)
        .all()
    )

    # Convert sections to dict format
    sections_data = [
        {"title": section.title, "content": section.content or ""}
        for section in sections
    ]

    try:
        # Generate DOCX
        docx_bytes = export_service.export_to_docx(
            report_title=report.title,
            sections=sections_data,
            author=current_user.name or current_user.email,
            metadata={"description": report.description},
        )

        # Generate filename
        filename = export_service.get_export_filename(report.title, "docx")

        # Return as streaming response
        return StreamingResponse(
            io.BytesIO(docx_bytes),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )

    except ImportError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate DOCX: {str(e)}",
        )


@router.get("/formats")
async def get_available_formats():
    """
    Get available export formats.

    Returns:
        List of available export formats
    """
    formats = []

    if export_service.reportlab_available:
        formats.append(
            {
                "format": "pdf",
                "name": "PDF Document",
                "extension": ".pdf",
                "available": True,
            }
        )
    else:
        formats.append(
            {
                "format": "pdf",
                "name": "PDF Document",
                "extension": ".pdf",
                "available": False,
                "message": "ReportLab not installed",
            }
        )

    if export_service.docx_available:
        formats.append(
            {
                "format": "docx",
                "name": "Word Document",
                "extension": ".docx",
                "available": True,
            }
        )
    else:
        formats.append(
            {
                "format": "docx",
                "name": "Word Document",
                "extension": ".docx",
                "available": False,
                "message": "python-docx not installed",
            }
        )

    return {"formats": formats}
