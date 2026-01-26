"""
Authentication service
"""

from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.schemas.auth import UserRegister, UserLogin, TokenPair


class AuthService:
    """Authentication service for user management"""

    @staticmethod
    def register_user(db: Session, user_data: UserRegister) -> User:
        """
        Register a new user.

        Args:
            db: Database session
            user_data: User registration data

        Returns:
            Created user

        Raises:
            HTTPException: If email already exists
        """
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Create new user
        user = User(
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            name=user_data.name,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def authenticate_user(db: Session, login_data: UserLogin) -> TokenPair:
        """
        Authenticate a user and return tokens.

        Args:
            db: Database session
            login_data: User login credentials

        Returns:
            Token pair (access and refresh tokens)

        Raises:
            HTTPException: If credentials are invalid
        """
        # Find user by email
        user = db.query(User).filter(User.email == login_data.email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        # Verify password
        if not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive"
            )

        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()

        # Create tokens
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})

        return TokenPair(access_token=access_token, refresh_token=refresh_token)

    @staticmethod
    def refresh_token(db: Session, refresh_token: str) -> TokenPair:
        """
        Refresh access token using refresh token.

        Args:
            db: Database session
            refresh_token: Refresh token

        Returns:
            New token pair

        Raises:
            HTTPException: If refresh token is invalid
        """
        payload = decode_token(refresh_token)

        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        # Check token type
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type"
            )

        user_id: Optional[str] = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        # Verify user exists and is active
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
            )

        # Create new tokens
        access_token = create_access_token(data={"sub": str(user.id)})
        new_refresh_token = create_refresh_token(data={"sub": str(user.id)})

        return TokenPair(access_token=access_token, refresh_token=new_refresh_token)

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """
        Get user by ID.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            User or None if not found
        """
        return db.query(User).filter(User.id == user_id).first()
