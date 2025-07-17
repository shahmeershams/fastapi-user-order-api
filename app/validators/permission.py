# app/validators/permission.py

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class PermissionBase(BaseModel):
    """Base Permission model with common fields"""
    name: str = Field(..., min_length=2, max_length=100, description="Display name of the permission")
    key: str = Field(..., min_length=2, max_length=50, description="Unique key for the permission")
    description: str = Field(..., min_length=5, max_length=300, description="Description of the permission")

class PermissionCreate(PermissionBase):
    """Permission creation model"""
    pass

class PermissionUpdate(BaseModel):
    """Permission update model - all fields optional"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    key: Optional[str] = Field(None, min_length=2, max_length=50)
    description: Optional[str] = Field(None, min_length=5, max_length=300)

class PermissionResponse(PermissionBase):
    """Permission response model"""
    model_config = ConfigDict(from_attributes=True)
    
    permission_id: int
    created_at: datetime

class PermissionListResponse(BaseModel):
    """Response model for permission list"""
    permissions: List[PermissionResponse]
    total: int
