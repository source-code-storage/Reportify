"""
Note management endpoints
"""

from typing import List
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    UploadFile,
    File,
    Form,
    Request,
)
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
import os
import uuid
import traceback

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.report import Report
from app.models.note import Note
from app.schemas.note import NoteResponse, NoteListResponse
from app.services.embedding_service import get_embedding_service
from app.services.vector_service import get_vector_service

router = APIRouter()


@router.post(
    "/upload", response_model=NoteResponse, status_code=status.HTTP_201_CREATED
)
async def upload_note(
    report_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload a note file and process it

    Supports: txt, pdf (text extraction coming soon)
    """
    print(f"DEBUG: Received report_id={report_id}, type={type(report_id)}")
    print(f"DEBUG: Received file={file.filename}, content_type={file.content_type}")
    # Verify report ownership
    report = (
        db.query(Report)
        .filter(Report.id == report_id, Report.user_id == current_user.id)
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Report not found"
        )

    # Validate file type
    file_ext = os.path.splitext(file.filename)[1].lower()
    allowed_extensions = [".txt", ".pdf", ".md"]

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file_ext} not supported. Allowed: {', '.join(allowed_extensions)}",
        )

    # Read file content
    content = await file.read()
    file_size = len(content)

    # Extract text based on file type
    if file_ext == ".txt" or file_ext == ".md":
        try:
            text_content = content.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File encoding not supported. Please use UTF-8.",
            )
    elif file_ext == ".pdf":
        # For now, return error. PDF extraction will be added later
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="PDF processing not yet implemented. Please use .txt files for now.",
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported file type"
        )

    # Create note record
    note = Note(
        report_id=report_id,
        user_id=current_user.id,
        filename=file.filename,
        file_type=file_ext[1:],  # Remove the dot
        file_size=file_size,
        file_path=f"notes/{uuid.uuid4()}/{file.filename}",  # Mock path for now
        content=text_content,
        status="processing",
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    # Process embeddings asynchronously (for now, do it synchronously)
    try:
        embedding_service = get_embedding_service()
        vector_service = get_vector_service()

        # Process note and generate embeddings
        chunks_and_embeddings = embedding_service.process_note_for_embedding(
            text_content
        )

        # Store embeddings in Qdrant
        chunks = [chunk for chunk, _ in chunks_and_embeddings]
        embeddings = [emb for _, emb in chunks_and_embeddings]

        qdrant_ids = vector_service.store_embeddings_batch(
            embeddings=embeddings,
            note_id=note.id,
            chunks=chunks,
            report_id=report_id,
            user_id=current_user.id,
            filename=file.filename,
            file_type=file_ext[1:],
        )

        # Update note status
        note.status = "completed"
        db.commit()
        db.refresh(note)

    except Exception as e:
        note.status = "failed"
        note.processing_error = str(e)
        db.commit()
        db.refresh(note)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process note: {str(e)}",
        )

    return note


@router.get("/", response_model=List[NoteListResponse])
def list_notes(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all notes for a report"""
    # Verify report ownership
    report = (
        db.query(Report)
        .filter(Report.id == report_id, Report.user_id == current_user.id)
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Report not found"
        )

    notes = db.query(Note).filter(Note.report_id == report_id).all()

    return notes


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific note"""
    note = (
        db.query(Note)
        .filter(Note.id == note_id, Note.user_id == current_user.id)
        .first()
    )

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )

    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a note"""
    note = (
        db.query(Note)
        .filter(Note.id == note_id, Note.user_id == current_user.id)
        .first()
    )

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )

    # Delete embeddings from Qdrant
    try:
        vector_service = get_vector_service()
        vector_service.delete_note_embeddings(note_id)
    except Exception as e:
        # Log error but continue with deletion
        print(f"Error deleting embeddings: {e}")

    db.delete(note)
    db.commit()

    return None
