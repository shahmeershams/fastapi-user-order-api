# app/validators/auth.py

from pydantic import BaseModel, Field
from typing import Optional
from .user import UserResponse

class TokenResponse(BaseModel):
    """Token response model for login and refresh endpoints"""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Access token expiry time in seconds")
    user: UserResponse = Field(..., description="User information")

class RefreshTokenRequest(BaseModel):
    """Request model for token refresh"""
    refresh_token: str = Field(..., description="Refresh token to exchange for new access token")

class LogoutRequest(BaseModel):
    """Request model for logout (optional - can be done with just headers)"""
    logout_all_devices: Optional[bool] = Field(False, description="Logout from all devices")

class CurrentUserResponse(UserResponse):
    """Response model for current user (/auth/me endpoint)"""
    permissions: Optional[list] = Field(default=[], description="User permissions")
    
class PasswordChangeRequest(BaseModel):
    """Request model for password change"""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, max_length=100, description="New password must be at least 8 characters")

class PasswordResetRequest(BaseModel):
    """Request model for password reset"""
    email: str = Field(..., description="Email address for password reset")

class TokenValidationResponse(BaseModel):
    """Response model for token validation"""
    valid: bool = Field(..., description="Whether token is valid")
    user_id: Optional[int] = Field(None, description="User ID if token is valid")
    role: Optional[str] = Field(None, description="User role if token is valid")
    expires_in: Optional[int] = Field(None, description="Seconds until token expires")
