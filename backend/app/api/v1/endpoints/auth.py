"""
Authentication endpoints
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.schemas.auth import (
    UserRegister,
    UserLogin,
    TokenPair,
    TokenRefresh,
    UserResponse,
)
from app.services.auth_service import AuthService
from app.models.user import User

router = APIRouter()


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user.

    Args:
        user_data: User registration data
        db: Database session

    Returns:
        Created user
    """
    user = AuthService.register_user(db, user_data)
    return user


@router.post("/login", response_model=TokenPair)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login and get access tokens.

    Args:
        login_data: User login credentials
        db: Database session

    Returns:
        Token pair (access and refresh tokens)
    """
    return AuthService.authenticate_user(db, login_data)


@router.post("/refresh", response_model=TokenPair)
def refresh(token_data: TokenRefresh, db: Session = Depends(get_db)):
    """
    Refresh access token using refresh token.

    Args:
        token_data: Refresh token
        db: Database session

    Returns:
        New token pair
    """
    return AuthService.refresh_token(db, token_data.refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(current_user: User = Depends(get_current_user)):
    """
    Logout user (client should discard tokens).

    Args:
        current_user: Current authenticated user

    Returns:
        No content
    """
    # In a stateless JWT system, logout is handled client-side
    # by discarding the tokens. This endpoint exists for consistency
    # and could be extended to maintain a token blacklist if needed.
    return None


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current user information.

    Args:
        current_user: Current authenticated user

    Returns:
        Current user data
    """
    return current_user
