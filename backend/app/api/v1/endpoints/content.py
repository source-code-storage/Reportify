"""
AI Content Generation endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.report import Report, ReportSection
from app.services.content_generation_service import get_content_generation_service

router = APIRouter()


class GenerateContentRequest(BaseModel):
    """Request model for content generation"""

    section_id: int
    section_description: Optional[str] = ""


class ImproveContentRequest(BaseModel):
    """Request model for content improvement"""

    section_id: int


class ExpandContentRequest(BaseModel):
    """Request model for content expansion"""

    section_id: int


class ContentGenerationResponse(BaseModel):
    """Response model for content generation"""

    content: str
    sources: List[Dict[str, Any]]
    metadata: Dict[str, Any]


@router.post("/generate", response_model=ContentGenerationResponse)
def generate_content(
    request: GenerateContentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate AI content for a section based on relevant notes

    This is the main AI feature! It:
    1. Finds relevant notes using semantic search
    2. Builds an intelligent prompt
    3. Calls GPT-4 to generate content
    4. Returns content with citations
    """
    # Get section
    section = (
        db.query(ReportSection).filter(ReportSection.id == request.section_id).first()
    )

    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Section not found"
        )

    # Verify report ownership
    report = (
        db.query(Report)
        .filter(Report.id == section.report_id, Report.user_id == current_user.id)
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found or access denied",
        )

    # Check if OpenAI API key is configured
    from app.core.config import settings

    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OpenAI API key not configured. Please set OPENAI_API_KEY in environment.",
        )

    # Generate content
    try:
        content_service = get_content_generation_service()

        result = content_service.generate_section_content(
            section_title=section.title,
            section_description=request.section_description or section.title,
            report_id=report.id,
            user_id=current_user.id,
        )

        # Optionally update the section with generated content
        # (commented out for now - let user decide whether to accept)
        # section.content = result['content']
        # section.word_count = len(result['content'].split())
        # db.commit()

        return ContentGenerationResponse(
            content=result["content"],
            sources=result["sources"],
            metadata=result["metadata"],
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Content generation failed: {str(e)}",
        )


@router.post("/improve", response_model=ContentGenerationResponse)
def improve_content(
    request: ImproveContentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Improve existing content using AI

    Takes the current section content and:
    - Enhances clarity and readability
    - Fixes grammar and style
    - Strengthens arguments
    - Ensures proper citations
    """
    # Get section
    section = (
        db.query(ReportSection).filter(ReportSection.id == request.section_id).first()
    )

    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Section not found"
        )

    # Verify report ownership
    report = (
        db.query(Report)
        .filter(Report.id == section.report_id, Report.user_id == current_user.id)
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found or access denied",
        )

    # Check if section has content
    if not section.content or section.content.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Section has no content to improve",
        )

    # Check if OpenAI API key is configured
    from app.core.config import settings

    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OpenAI API key not configured",
        )

    # Improve content
    try:
        content_service = get_content_generation_service()

        result = content_service.improve_content(
            section_title=section.title,
            current_content=section.content,
            report_id=report.id,
            user_id=current_user.id,
        )

        return ContentGenerationResponse(
            content=result["content"],
            sources=result["sources"],
            metadata=result["metadata"],
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Content improvement failed: {str(e)}",
        )


@router.post("/expand", response_model=ContentGenerationResponse)
def expand_content(
    request: ExpandContentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Expand existing content with more detail using AI

    Takes the current section content and:
    - Adds more detail and depth
    - Incorporates additional information
    - Elaborates on key points
    - Adds examples or evidence
    """
    # Get section
    section = (
        db.query(ReportSection).filter(ReportSection.id == request.section_id).first()
    )

    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Section not found"
        )

    # Verify report ownership
    report = (
        db.query(Report)
        .filter(Report.id == section.report_id, Report.user_id == current_user.id)
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found or access denied",
        )

    # Check if section has content
    if not section.content or section.content.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Section has no content to expand",
        )

    # Check if OpenAI API key is configured
    from app.core.config import settings

    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OpenAI API key not configured",
        )

    # Expand content
    try:
        content_service = get_content_generation_service()

        result = content_service.expand_content(
            section_title=section.title,
            current_content=section.content,
            report_id=report.id,
            user_id=current_user.id,
        )

        return ContentGenerationResponse(
            content=result["content"],
            sources=result["sources"],
            metadata=result["metadata"],
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Content expansion failed: {str(e)}",
        )


@router.get("/search")
def search_notes(
    query: str,
    report_id: int,
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Search notes using semantic search

    Finds notes relevant to the query using AI embeddings
    """
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

    try:
        from app.services.embedding_service import get_embedding_service
        from app.services.vector_service import get_vector_service

        print(f"Searching for: {query} in report {report_id}")

        # Generate query embedding
        embedding_service = get_embedding_service()
        query_embedding = embedding_service.generate_embedding(query)
        print(f"Generated embedding with dimension: {len(query_embedding)}")

        # Search for similar notes
        vector_service = get_vector_service()
        results = vector_service.search_similar(
            query_embedding=query_embedding,
            report_id=report_id,
            user_id=current_user.id,
            limit=limit,
        )

        print(f"Found {len(results)} results")

        return {"query": query, "results": results}

    except Exception as e:
        import traceback

        print(f"Search error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}",
        )
