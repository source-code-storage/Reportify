"""
Main API router for v1
"""

from fastapi import APIRouter
from app.api.v1.endpoints import auth, reports, notes, content, uploads, export

api_router = APIRouter()

# Include authentication endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

# Include report management endpoints
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])

# Include note management endpoints
api_router.include_router(notes.router, prefix="/notes", tags=["notes"])

# Include AI content generation endpoints
api_router.include_router(
    content.router, prefix="/content", tags=["content-generation"]
)

# Include file upload endpoints
api_router.include_router(uploads.router, prefix="/uploads", tags=["uploads"])

# Include export endpoints
api_router.include_router(export.router, prefix="/export", tags=["export"])


@api_router.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Report Writing Assistant API v1",
        "endpoints": {
            "auth": "/api/v1/auth",
            "reports": "/api/v1/reports",
            "notes": "/api/v1/notes",
            "content": "/api/v1/content",
            "uploads": "/api/v1/uploads",
            "export": "/api/v1/export",
        },
    }
