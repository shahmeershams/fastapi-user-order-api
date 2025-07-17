# app/validators/role.py

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class RoleBase(BaseModel):
    """Base Role model with common fields"""
    name: str = Field(..., min_length=2, max_length=100, description="Display name of the role")
    key: str = Field(..., min_length=2, max_length=50, description="Unique key for the role")
    description: str = Field(..., min_length=5, max_length=300, description="Description of the role")

class RoleCreate(RoleBase):
    """Role creation model"""
    pass

class RoleUpdate(BaseModel):
    """Role update model - all fields optional"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    key: Optional[str] = Field(None, min_length=2, max_length=50)
    description: Optional[str] = Field(None, min_length=5, max_length=300)

class RoleResponse(RoleBase):
    """Role response model"""
    model_config = ConfigDict(from_attributes=True)
    
    role_id: int
    created_at: datetime

class RoleWithPermissionsResponse(RoleResponse):
    """Role response with permissions"""
    permissions: List['PermissionResponse'] = []

class RoleListResponse(BaseModel):
    """Response model for role list"""
    roles: List[RoleResponse]
    total: int
