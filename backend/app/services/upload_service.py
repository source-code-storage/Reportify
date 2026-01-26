"""
Upload service for handling file uploads
"""

from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status

from app.models.upload_job import UploadJob
from app.models.note import Note
from app.services.storage_service import storage_service
from app.services.file_validation_service import file_validation_service


class UploadService:
    """Service for managing file uploads"""

    @staticmethod
    async def upload_template(
        db: Session, report_id: int, user_id: int, file: UploadFile
    ) -> UploadJob:
        """
        Upload a report template file.

        Args:
            db: Database session
            report_id: Report ID
            user_id: User ID
            file: Uploaded file

        Returns:
            UploadJob tracking the upload

        Raises:
            HTTPException: If validation or upload fails
        """
        # Validate file
        mime_type, file_size = await file_validation_service.validate_upload_file(file)

        # Sanitize filename
        safe_filename = file_validation_service.sanitize_filename(file.filename)

        # Create upload job
        upload_job = UploadJob(
            report_id=report_id,
            user_id=user_id,
            filename=safe_filename,
            file_type="template",
            file_format=mime_type.split("/")[-1],
            file_size=file_size,
            status="uploading",
            progress=0,
        )

        db.add(upload_job)
        db.commit()
        db.refresh(upload_job)

        try:
            # Read file content
            content = await file.read()

            # Upload to S3
            object_key = storage_service.upload_file(
                file_content=content,
                file_name=safe_filename,
                content_type=mime_type,
                folder=f"templates/{report_id}",
            )

            # Update upload job
            upload_job.file_path = object_key
            upload_job.status = "queued"
            upload_job.progress = 50
            db.commit()

            # Trigger async PDF processing
            from app.worker.tasks.pdf_processing import process_template

            process_template.delay(upload_job.id)

            db.refresh(upload_job)
            return upload_job

        except Exception as e:
            upload_job.status = "failed"
            upload_job.error_message = str(e)
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to upload template: {str(e)}",
            )

    @staticmethod
    async def upload_note(
        db: Session, report_id: int, user_id: int, file: UploadFile
    ) -> UploadJob:
        """
        Upload a note file.

        Args:
            db: Database session
            report_id: Report ID
            user_id: User ID
            file: Uploaded file

        Returns:
            UploadJob tracking the upload

        Raises:
            HTTPException: If validation or upload fails
        """
        # Validate file
        mime_type, file_size = await file_validation_service.validate_upload_file(file)

        # Sanitize filename
        safe_filename = file_validation_service.sanitize_filename(file.filename)

        # Get file category
        file_category = file_validation_service.get_file_category(safe_filename)

        # Create upload job
        upload_job = UploadJob(
            report_id=report_id,
            user_id=user_id,
            filename=safe_filename,
            file_type="note",
            file_format=mime_type.split("/")[-1],
            file_size=file_size,
            status="uploading",
            progress=0,
        )

        db.add(upload_job)
        db.commit()
        db.refresh(upload_job)

        try:
            # Read file content
            content = await file.read()

            # Upload to S3
            object_key = storage_service.upload_file(
                file_content=content,
                file_name=safe_filename,
                content_type=mime_type,
                folder=f"notes/{report_id}",
            )

            # Update upload job
            upload_job.file_path = object_key
            upload_job.status = "queued"
            upload_job.progress = 50
            db.commit()

            # Create Note record
            note = Note(
                report_id=report_id,
                user_id=user_id,
                filename=safe_filename,
                file_type=file_category,
                file_size=file_size,
                file_path=object_key,
                content="",  # Will be filled by processing
                status="pending",
            )

            db.add(note)
            db.commit()
            db.refresh(note)

            # Link note to upload job
            upload_job.note_id = note.id
            db.commit()

            # Trigger async OCR/text extraction
            from app.worker.tasks.ocr_processing import process_note

            process_note.delay(upload_job.id)

            db.refresh(upload_job)
            return upload_job

        except Exception as e:
            upload_job.status = "failed"
            upload_job.error_message = str(e)
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to upload note: {str(e)}",
            )

    @staticmethod
    def get_upload_status(db: Session, upload_id: int, user_id: int) -> UploadJob:
        """
        Get upload job status.

        Args:
            db: Database session
            upload_id: Upload job ID
            user_id: User ID (for authorization)

        Returns:
            UploadJob

        Raises:
            HTTPException: If upload job not found or unauthorized
        """
        upload_job = (
            db.query(UploadJob)
            .filter(UploadJob.id == upload_id, UploadJob.user_id == user_id)
            .first()
        )

        if not upload_job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Upload job not found",
            )

        return upload_job

    @staticmethod
    def delete_upload(db: Session, upload_id: int, user_id: int) -> bool:
        """
        Delete an upload job and associated file.

        Args:
            db: Database session
            upload_id: Upload job ID
            user_id: User ID (for authorization)

        Returns:
            True if deleted

        Raises:
            HTTPException: If upload job not found or unauthorized
        """
        upload_job = UploadService.get_upload_status(db, upload_id, user_id)

        # Delete file from S3 if it exists
        if upload_job.file_path:
            try:
                storage_service.delete_file(upload_job.file_path)
            except Exception as e:
                print(f"Error deleting file from S3: {e}")

        # Delete upload job
        db.delete(upload_job)
        db.commit()

        return True
