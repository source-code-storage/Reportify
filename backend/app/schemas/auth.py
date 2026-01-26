"""
Authentication schemas
"""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    """User registration request"""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    name: str = Field(..., min_length=1, max_length=255)


class UserLogin(BaseModel):
    """User login request"""

    email: EmailStr
    password: str


class TokenPair(BaseModel):
    """Token pair response"""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    """Token refresh request"""

    refresh_token: str


class UserResponse(BaseModel):
    """User response"""

    id: int  # Changed from UUID to int to match the database model
    email: str
    name: str
    created_at: datetime
    last_login: datetime | None
    is_active: bool

    class Config:
        from_attributes = True
