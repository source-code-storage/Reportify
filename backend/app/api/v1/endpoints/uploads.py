"""
File upload endpoints
"""

from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.upload_job import UploadJob
from app.services.storage_service import storage_service
from app.services.file_validation_service import file_validation_service

router = APIRouter()


@router.post("/template", status_code=status.HTTP_201_CREATED)
async def upload_template(
    report_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload a report template (PDF).

    Args:
        report_id: ID of the report this template belongs to
        file: Template file (PDF)
        db: Database session
        current_user: Current authenticated user

    Returns:
        Upload job details
    """
    from app.services.upload_service import UploadService

    # Use the upload service which handles PDF processing
    upload_job = await UploadService.upload_template(
        db=db, report_id=report_id, user_id=current_user.id, file=file
    )

    return {
        "id": upload_job.id,
        "filename": upload_job.filename,
        "file_type": upload_job.file_type,
        "file_size": upload_job.file_size,
        "status": upload_job.status,
        "message": "Template uploaded successfully. Processing will begin shortly.",
    }


@router.post("/notes", status_code=status.HTTP_201_CREATED)
async def upload_notes(
    report_id: int = Form(...),
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload multiple note files (PDF, TXT, images).

    Args:
        report_id: ID of the report these notes belong to
        files: List of note files
        db: Database session
        current_user: Current authenticated user

    Returns:
        List of upload job details
    """
    # Verify report ownership
    from app.services.report_service import ReportService

    report = ReportService.get_report(db, report_id, current_user.id)

    upload_jobs = []

    for file in files:
        try:
            # Validate file
            mime_type, file_size = await file_validation_service.validate_upload_file(
                file
            )

            # Upload file to S3
            file_content = await file.read()
            object_key = storage_service.upload_file(
                file_content=file_content,
                file_name=file.filename or "note",
                content_type=mime_type,
                folder=f"notes/{report_id}",
            )

            # Create upload job
            upload_job = UploadJob(
                user_id=current_user.id,
                report_id=report_id,
                filename=file.filename or "note",
                file_type="note",
                file_format=file_validation_service.get_file_type(file.filename or ""),
                file_size=file_size,
                file_path=object_key,
                status="completed",  # For now, mark as completed immediately
                progress=100,
            )

            db.add(upload_job)
            upload_jobs.append(upload_job)

        except HTTPException as e:
            # If one file fails, continue with others
            upload_job = UploadJob(
                user_id=current_user.id,
                report_id=report_id,
                filename=file.filename or "note",
                file_type="note",
                file_format=file_validation_service.get_file_type(file.filename or ""),
                file_size=0,
                status="failed",
                error_message=e.detail,
            )
            db.add(upload_job)
            upload_jobs.append(upload_job)

    db.commit()

    # Refresh all jobs
    for job in upload_jobs:
        db.refresh(job)

    return {
        "uploaded": len([j for j in upload_jobs if j.status == "completed"]),
        "failed": len([j for j in upload_jobs if j.status == "failed"]),
        "jobs": [
            {
                "id": job.id,
                "filename": job.filename,
                "file_type": job.file_type,
                "file_size": job.file_size,
                "status": job.status,
                "error_message": job.error_message,
            }
            for job in upload_jobs
        ],
    }


@router.get("/{upload_id}/status")
async def get_upload_status(
    upload_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get the status of an upload job.

    Args:
        upload_id: Upload job ID
        db: Database session
        current_user: Current authenticated user

    Returns:
        Upload job status
    """
    upload_job = (
        db.query(UploadJob)
        .filter(UploadJob.id == upload_id, UploadJob.user_id == current_user.id)
        .first()
    )

    if not upload_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Upload job not found"
        )

    return {
        "id": upload_job.id,
        "filename": upload_job.filename,
        "file_type": upload_job.file_type,
        "status": upload_job.status,
        "progress": upload_job.progress,
        "error_message": upload_job.error_message,
        "created_at": upload_job.created_at,
        "completed_at": upload_job.completed_at,
    }


@router.delete("/{upload_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_upload(
    upload_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete an upload job and its associated file.

    Args:
        upload_id: Upload job ID
        db: Database session
        current_user: Current authenticated user

    Returns:
        No content
    """
    upload_job = (
        db.query(UploadJob)
        .filter(UploadJob.id == upload_id, UploadJob.user_id == current_user.id)
        .first()
    )

    if not upload_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Upload job not found"
        )

    # Delete file from S3 if it exists
    if upload_job.file_path:
        try:
            storage_service.delete_file(upload_job.file_path)
        except Exception as e:
            # Log error but continue with database deletion
            print(f"Error deleting file from S3: {e}")

    # Delete upload job from database
    db.delete(upload_job)
    db.commit()

    return None
