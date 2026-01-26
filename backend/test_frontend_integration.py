"""
Simple test to verify frontend can connect to backend
This creates a minimal FastAPI server without database dependency
"""

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uvicorn

app = FastAPI(title="Report Writing Assistant - Test Server")

# CORS middleware - Allow both ports for flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    created_at: str
    is_active: bool


class ReportResponse(BaseModel):
    id: str
    title: str
    description: str
    created_at: str
    updated_at: str
    progress_percentage: int
    total_word_count: int
    status: str
    user_id: str


class ReportSectionResponse(BaseModel):
    id: str
    report_id: str
    title: str
    content: str
    order: int
    word_count: int
    is_completed: bool


class ReportDetailResponse(BaseModel):
    report: ReportResponse
    sections: List[ReportSectionResponse]


# Mock data storage
mock_reports = [
    {
        "id": "1",
        "title": "Internship Final Report",
        "description": "Final report for summer internship at Tech Corp",
        "created_at": "2024-01-05T10:00:00",
        "updated_at": "2024-01-08T15:30:00",
        "progress_percentage": 65,
        "total_word_count": 3500,
        "status": "in_progress",
        "user_id": "test-user-id-123",
    },
    {
        "id": "2",
        "title": "Research Project Report",
        "description": "Machine Learning research findings",
        "created_at": "2024-01-02T09:00:00",
        "updated_at": "2024-01-07T14:20:00",
        "progress_percentage": 30,
        "total_word_count": 1200,
        "status": "draft",
        "user_id": "test-user-id-123",
    },
    {
        "id": "3",
        "title": "Thesis Chapter 3",
        "description": "Methodology and implementation details",
        "created_at": "2023-12-20T11:00:00",
        "updated_at": "2024-01-06T16:45:00",
        "progress_percentage": 90,
        "total_word_count": 5800,
        "status": "in_progress",
        "user_id": "test-user-id-123",
    },
]

mock_sections = {
    "1": [
        {
            "id": "s1",
            "report_id": "1",
            "title": "Introduction",
            "content": "This is the introduction section...",
            "order": 1,
            "word_count": 250,
            "is_completed": True,
        },
        {
            "id": "s2",
            "report_id": "1",
            "title": "Background",
            "content": "Background information about the internship...",
            "order": 2,
            "word_count": 500,
            "is_completed": True,
        },
        {
            "id": "s3",
            "report_id": "1",
            "title": "Methodology",
            "content": "",
            "order": 3,
            "word_count": 0,
            "is_completed": False,
        },
        {
            "id": "s4",
            "report_id": "1",
            "title": "Results",
            "content": "Key findings and results...",
            "order": 4,
            "word_count": 800,
            "is_completed": False,
        },
        {
            "id": "s5",
            "report_id": "1",
            "title": "Conclusion",
            "content": "",
            "order": 5,
            "word_count": 0,
            "is_completed": False,
        },
    ]
}


@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Test server running"}


@app.post("/api/v1/auth/register", response_model=UserResponse)
def register(data: RegisterRequest):
    """Mock registration endpoint"""
    return {
        "id": "test-user-id-123",
        "email": data.email,
        "name": data.name,
        "created_at": "2024-01-08T12:00:00",
        "is_active": True,
    }


@app.post("/api/v1/auth/login", response_model=TokenResponse)
def login(data: LoginRequest):
    """Mock login endpoint"""
    # Accept any credentials for testing
    return {
        "access_token": "mock-access-token-12345",
        "refresh_token": "mock-refresh-token-67890",
        "token_type": "bearer",
    }


@app.get("/api/v1/auth/me", response_model=UserResponse)
def get_current_user():
    """Mock get current user endpoint"""
    return {
        "id": "test-user-id-123",
        "email": "test@example.com",
        "name": "Test User",
        "created_at": "2024-01-08T12:00:00",
        "is_active": True,
    }


@app.post("/api/v1/auth/logout")
def logout():
    """Mock logout endpoint"""
    return {"message": "Logged out successfully"}


@app.post("/api/v1/auth/refresh", response_model=TokenResponse)
def refresh_token():
    """Mock token refresh endpoint"""
    return {
        "access_token": "mock-new-access-token-12345",
        "refresh_token": "mock-new-refresh-token-67890",
        "token_type": "bearer",
    }


@app.get("/api/v1/reports", response_model=List[ReportResponse])
def get_reports():
    """Mock get all reports endpoint"""
    return mock_reports


@app.get("/api/v1/reports/{report_id}", response_model=ReportDetailResponse)
def get_report(report_id: str):
    """Mock get report by ID endpoint"""
    report = next((r for r in mock_reports if r["id"] == report_id), None)
    if not report:
        return {"report": None, "sections": []}

    sections = mock_sections.get(report_id, [])
    return {"report": report, "sections": sections}


@app.post("/api/v1/reports", response_model=ReportResponse)
async def create_report(
    title: str = Form(...),
    description: str = Form(...),
    template: Optional[UploadFile] = File(None),
):
    """Mock create report endpoint"""
    new_id = str(len(mock_reports) + 1)
    new_report = {
        "id": new_id,
        "title": title,
        "description": description,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "progress_percentage": 0,
        "total_word_count": 0,
        "status": "draft",
        "user_id": "test-user-id-123",
    }
    mock_reports.insert(0, new_report)

    # Create default sections if template was uploaded
    if template:
        mock_sections[new_id] = [
            {
                "id": f"s{new_id}-1",
                "report_id": new_id,
                "title": "Introduction",
                "content": "",
                "order": 1,
                "word_count": 0,
                "is_completed": False,
            },
            {
                "id": f"s{new_id}-2",
                "report_id": new_id,
                "title": "Main Content",
                "content": "",
                "order": 2,
                "word_count": 0,
                "is_completed": False,
            },
            {
                "id": f"s{new_id}-3",
                "report_id": new_id,
                "title": "Conclusion",
                "content": "",
                "order": 3,
                "word_count": 0,
                "is_completed": False,
            },
        ]

    return new_report


@app.put("/api/v1/reports/{report_id}", response_model=ReportResponse)
def update_report(report_id: str, data: dict):
    """Mock update report endpoint"""
    report = next((r for r in mock_reports if r["id"] == report_id), None)
    if report:
        report.update(data)
        report["updated_at"] = datetime.now().isoformat()
    return report


@app.delete("/api/v1/reports/{report_id}")
def delete_report(report_id: str):
    """Mock delete report endpoint"""
    global mock_reports
    mock_reports = [r for r in mock_reports if r["id"] != report_id]
    if report_id in mock_sections:
        del mock_sections[report_id]
    return {"message": "Report deleted successfully"}


@app.put(
    "/api/v1/reports/{report_id}/sections/{section_id}",
    response_model=ReportSectionResponse,
)
def update_section(report_id: str, section_id: str, data: dict):
    """Mock update section endpoint"""
    sections = mock_sections.get(report_id, [])
    section = next((s for s in sections if s["id"] == section_id), None)
    if section:
        section["content"] = data.get("content", section["content"])
        section["word_count"] = len(section["content"].split())
        section["is_completed"] = section["word_count"] > 0
    return section


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Starting Test Backend Server")
    print("=" * 60)
    print("Frontend: http://localhost:5173")
    print("Backend:  http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("=" * 60)
    print("\n✅ This is a MOCK server for testing the frontend")
    print("✅ It accepts any credentials and returns mock data")
    print("✅ Perfect for testing the UI without database!\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)
