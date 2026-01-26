"""
OCR processing tasks
"""

import os
import tempfile
from datetime import datetime
from sqlalchemy.orm import Session

from app.worker.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.note import Note
from app.models.upload_job import UploadJob
from app.services.ocr_service import ocr_service
from app.services.storage_service import storage_service


@celery_app.task(name="app.worker.tasks.ocr.process_note", bind=True)
def process_note(self, upload_job_id: int):
    """
    Process note file to extract text using OCR or direct extraction.

    Args:
        upload_job_id: ID of the upload job

    Returns:
        dict: Processing result with extracted text
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

        # Get note if it exists
        note = None
        if upload_job.note_id:
            note = db.query(Note).filter(Note.id == upload_job.note_id).first()

        if not note:
            # Create note record
            note = Note(
                report_id=upload_job.report_id,
                user_id=upload_job.user_id,
                filename=upload_job.filename,
                file_type=upload_job.file_format,
                file_size=upload_job.file_size,
                file_path=upload_job.file_path,
                content="",
                status="processing",
            )
            db.add(note)
            db.flush()

            # Link to upload job
            upload_job.note_id = note.id
            db.commit()

        # Update progress
        upload_job.progress = 20
        db.commit()

        # Download file from S3 to temporary file
        file_extension = os.path.splitext(upload_job.filename)[1].lower()

        with tempfile.NamedTemporaryFile(
            delete=False, suffix=file_extension
        ) as tmp_file:
            tmp_path = tmp_file.name
            try:
                # Download file from S3
                file_content = storage_service.download_file(upload_job.file_path)
                tmp_file.write(file_content)
                tmp_file.flush()

                # Update progress
                upload_job.progress = 40
                db.commit()

                # Extract text based on file type
                extracted_text = ""
                metadata = {}

                if file_extension == ".txt":
                    # Plain text file
                    extracted_text = file_content.decode("utf-8", errors="ignore")
                    metadata = {
                        "word_count": len(extracted_text.split()),
                        "char_count": len(extracted_text),
                    }

                elif file_extension == ".pdf":
                    # Check if PDF is scanned or text-based
                    if ocr_service.is_scanned_pdf(tmp_path):
                        # Scanned PDF - use OCR
                        extracted_text, metadata = (
                            ocr_service.extract_text_from_pdf_images(tmp_path)
                        )
                    else:
                        # Text-based PDF - use direct extraction
                        import fitz

                        doc = fitz.open(tmp_path)
                        extracted_text = ""
                        for page in doc:
                            extracted_text += page.get_text() + "\n"
                        doc.close()
                        metadata = {
                            "word_count": len(extracted_text.split()),
                            "char_count": len(extracted_text),
                        }

                elif ocr_service.is_image_file(upload_job.filename):
                    # Image file - use OCR
                    extracted_text, metadata = ocr_service.extract_text_from_image(
                        tmp_path
                    )

                else:
                    raise Exception(f"Unsupported file type: {file_extension}")

                # Update progress
                upload_job.progress = 80
                db.commit()

                # Update note with extracted content
                note.content = extracted_text.strip()
                note.status = "completed"
                db.commit()

                # Update upload job
                upload_job.status = "completed"
                upload_job.progress = 100
                upload_job.completed_at = datetime.utcnow()
                db.commit()

                return {
                    "status": "success",
                    "note_id": note.id,
                    "word_count": metadata.get("word_count", 0),
                    "confidence": metadata.get("confidence", 0),
                    "message": "Note processed successfully",
                }

            finally:
                # Clean up temporary file
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

    except Exception as e:
        # Update upload job and note with error
        upload_job.status = "failed"
        upload_job.error_message = str(e)

        if note:
            note.status = "failed"
            note.processing_error = str(e)

        db.commit()

        return {"status": "error", "message": str(e)}

    finally:
        db.close()
