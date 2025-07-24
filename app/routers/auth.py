# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services import AuthService
from app.validators import (
    UserLogin, TokenResponse, RefreshTokenRequest, 
    CurrentUserResponse, LogoutRequest
)
from typing import Optional

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login user with username/email and password.
    
    Returns JWT access and refresh tokens with user information.
    
    - **username**: Username or email address
    - **password**: User password
    """
    return AuthService.login(db, credentials)

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(refresh_request: RefreshTokenRequest, db: Session = Depends(get_db)):
    """
    Refresh access token using refresh token.
    
    Exchanges a valid refresh token for a new access token and refresh token pair.
    
    - **refresh_token**: Valid refresh token received from login
    """
    return AuthService.refresh_access_token(db, refresh_request.refresh_token)

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Logout user by invalidating all tokens.
    
    Requires Authorization header with Bearer token.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required"
        )
    
    token = authorization.split(" ")[1]
    
    # Get user from token
    user = AuthService.get_current_user_from_token(db, token)
    
    # Invalidate all tokens for this user
    AuthService.logout(db, user.user_id)
    
    return None

@router.get("/me", response_model=CurrentUserResponse)
def get_current_user_info(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Get current user information from JWT token.
    
    Returns detailed user information including role and permissions.
    Requires Authorization header with Bearer token.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required"
        )
    
    token = authorization.split(" ")[1]
    
    # Get user from token with role information
    user = AuthService.get_current_user_from_token(db, token)
    
    # Get user permissions (we'll implement this later)
    permissions = []
    
    # Create response with permissions
    user_response = CurrentUserResponse.model_validate(user)
    user_response.permissions = permissions
    
    return user_response

@router.post("/validate", response_model=dict)
def validate_token(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Validate JWT token and return token information.
    
    Used by other services to verify token validity.
    Requires Authorization header with Bearer token.
    """
    if not authorization or not authorization.startswith("Bearer "):
        return {"valid": False, "error": "Authorization header required"}
    
    token = authorization.split(" ")[1]
    
    try:
        user = AuthService.get_current_user_from_token(db, token)
        return {
            "valid": True,
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "role": user.role.key,
            "role_id": user.role_id
        }
    except HTTPException:
        return {"valid": False, "error": "Invalid or expired token"}

@router.post("/cleanup", status_code=status.HTTP_200_OK)
def cleanup_expired_tokens(db: Session = Depends(get_db)):
    """
    Clean up expired tokens from database.
    
    This endpoint can be called periodically to remove expired tokens.
    In production, this should be protected or run as a scheduled task.
    """
    cleaned_count = AuthService.cleanup_expired_tokens(db)
    return {"message": f"Cleaned up {cleaned_count} expired tokens"}
