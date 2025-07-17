# app/validators/user.py

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from .role import RoleResponse
from .order import OrderResponse

class UserBase(BaseModel):
    """Base User model with common fields"""
    username: str = Field(..., min_length=3, max_length=30, description="Username must be between 3-30 characters")
    email: EmailStr = Field(..., description="Valid email address")

class UserCreate(UserBase):
    """User creation model"""
    password: str = Field(..., min_length=8, max_length=100, description="Password must be at least 8 characters")
    role_id: Optional[int] = Field(None, description="Role ID - if not provided, defaults to customer role")

class UserLogin(BaseModel):
    """User login model"""
    username: str = Field(..., description="Username or email")
    password: str = Field(..., description="User password")

class UserUpdate(BaseModel):
    """User update model - all fields optional"""
    username: Optional[str] = Field(None, min_length=3, max_length=30)
    email: Optional[EmailStr] = Field(None)
    password: Optional[str] = Field(None, min_length=8, max_length=100)

class UserResponse(UserBase):
    """User response model"""
    model_config = ConfigDict(from_attributes=True)
    
    user_id: int
    role_id: int
    created_at: datetime
    role: Optional[RoleResponse] = None

class UserWithOrdersResponse(UserResponse):
    """User response with orders"""
    orders: List[OrderResponse] = []

class UserProfileResponse(UserResponse):
    """User profile response (for /users/me endpoint)"""
    pass

class UserListResponse(BaseModel):
    """Response model for user list"""
    users: List[UserResponse]
    total: int
    page: int
    per_page: int
