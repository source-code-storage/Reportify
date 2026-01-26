"""
PDF processing tasks
"""

import os
import tempfile
from datetime import datetime
from sqlalchemy.orm import Session

from app.worker.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.template_structure import TemplateStructure, TemplateSection
from app.models.upload_job import UploadJob
from app.models.report import Report, ReportSection
from app.services.pdf_service import pdf_service
from app.services.storage_service import storage_service


@celery_app.task(name="app.worker.tasks.pdf.process_template", bind=True)
def process_template(self, upload_job_id: int):
    """
    Process PDF template to extract structure.

    Args:
        upload_job_id: ID of the upload job

    Returns:
        dict: Processing result with structure information
    """
    db = SessionLocal()

    try:
        # Get upload job
        upload_job = db.query(UploadJob).filter(UploadJob.id == upload_job_id).first()
        if not upload_job:
            return {"status": "error", "message": "Upload job not found"}

        # Update upload job status
        upload_job.status = "processing"
        upload_job.progress = 10
        db.commit()

        # Get report
        report = db.query(Report).filter(Report.id == upload_job.report_id).first()
        if not report:
            upload_job.status = "failed"
            upload_job.error_message = "Report not found"
            db.commit()
            return {"status": "error", "message": "Report not found"}

        # Download PDF from S3 to temporary file
        upload_job.progress = 20
        db.commit()

        # Create temporary file
        tmp_fd, tmp_path = tempfile.mkstemp(suffix=".pdf")
        try:
            # Download file from S3
            file_content = storage_service.download_file(upload_job.file_path)

            # Write to temporary file and close it properly
            os.write(tmp_fd, file_content)
            os.close(tmp_fd)  # Close the file descriptor

            # Update progress
            upload_job.progress = 40
            db.commit()

            # Extract text and structure from PDF
            full_text, text_blocks, metadata = pdf_service.extract_text_from_pdf(
                tmp_path
            )

            # Update progress
            upload_job.progress = 60
            db.commit()

            # Identify sections
            sections = pdf_service.identify_sections(text_blocks)

            # Update progress
            upload_job.progress = 80
            db.commit()

            # Create TemplateStructure record
            template_structure = TemplateStructure(
                report_id=report.id,
                upload_job_id=upload_job.id,
                filename=upload_job.filename,
                file_path=upload_job.file_path,
                total_pages=metadata.get("total_pages", 0),
                full_text=full_text,
                metadata=metadata,
                status="completed",
                processed_at=datetime.utcnow(),
            )
            db.add(template_structure)
            db.flush()  # Get the ID

            # Create TemplateSection records
            _save_sections_recursive(
                db, template_structure.id, sections, parent_id=None, order=0
            )

            # Create ReportSection records from template sections
            _create_report_sections_from_template(db, report.id, template_structure.id)

            # Update upload job
            upload_job.status = "completed"
            upload_job.progress = 100
            upload_job.completed_at = datetime.utcnow()

            # Commit all changes
            db.commit()

            return {
                "status": "success",
                "template_id": template_structure.id,
                "total_pages": metadata.get("total_pages", 0),
                "sections_count": len(sections),
                "message": "PDF processed successfully",
            }

        finally:
            # Clean up temporary file
            try:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
            except Exception as cleanup_error:
                print(
                    f"Warning: Could not delete temp file {tmp_path}: {cleanup_error}"
                )

    except Exception as e:
        # Update upload job with error
        upload_job.status = "failed"
        upload_job.error_message = str(e)
        db.commit()

        return {"status": "error", "message": str(e)}

    finally:
        db.close()


def _save_sections_recursive(
    db: Session, template_id: int, sections: list, parent_id: int = None, order: int = 0
) -> int:
    """
    Recursively save sections and their children.

    Args:
        db: Database session
        template_id: Template structure ID
        sections: List of PDFSection objects
        parent_id: Parent section ID (None for root sections)
        order: Starting order number

    Returns:
        Next order number
    """
    current_order = order

    for section in sections:
        # Create section record
        template_section = TemplateSection(
            template_id=template_id,
            parent_id=parent_id,
            level=section.level,
            order=current_order,
            title=section.title,
            content=section.content,
            page_number=section.page_number,
            position_top=section.position_top,
            font_size=section.font_size,
            font_name=section.font_name,
            is_bold=1 if section.is_bold else 0,
            word_count=section.word_count,
        )
        db.add(template_section)
        db.flush()  # Get the ID

        # Save children recursively
        if section.children:
            _save_sections_recursive(
                db,
                template_id,
                section.children,
                parent_id=template_section.id,
                order=0,
            )

        current_order += 1

    return current_order


def _create_report_sections_from_template(
    db: Session, report_id: int, template_id: int
):
    """
    Create ReportSection records from TemplateSection records.

    Args:
        db: Database session
        report_id: Report ID
        template_id: Template structure ID
    """
    # Get all template sections for this template
    template_sections = (
        db.query(TemplateSection)
        .filter(TemplateSection.template_id == template_id)
        .order_by(TemplateSection.order)
        .all()
    )

    # Create report sections from template sections
    for template_section in template_sections:
        report_section = ReportSection(
            report_id=report_id,
            title=template_section.title,
            content=template_section.content or "",
            order=template_section.order,
            word_count=template_section.word_count,
            is_completed=False,
        )
        db.add(report_section)

    db.flush()
