# app/routers/roles.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services import RoleService
from app.validators import RoleCreate, RoleUpdate, RoleResponse, RoleListResponse
from typing import List

router = APIRouter(prefix="/roles", tags=["roles"])

@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    """
    Create a new role.
    
    - **name**: Display name for the role (e.g., "Administrator")
    - **key**: Unique identifier for the role (e.g., "admin")
    - **description**: Description of what this role does
    """
    return RoleService.create_role(db, role)

@router.get("/", response_model=RoleListResponse)
def list_roles(db: Session = Depends(get_db)):
    """
    Get all roles in the system.
    
    Returns a list of all available roles with their details.
    """
    return RoleService.list_roles(db)

@router.get("/{role_id}", response_model=RoleResponse)
def get_role(role_id: int, db: Session = Depends(get_db)):
    """
    Get a specific role by ID.
    
    - **role_id**: The ID of the role to retrieve
    """
    return RoleService.get_role(db, role_id)

@router.put("/{role_id}", response_model=RoleResponse)
def update_role(role_id: int, role_update: RoleUpdate, db: Session = Depends(get_db)):
    """
    Update a role's information.
    
    - **role_id**: The ID of the role to update
    - **role_update**: Fields to update (all optional)
    """
    return RoleService.update_role(db, role_id, role_update)

@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    """
    Delete a role.
    
    - **role_id**: The ID of the role to delete
    
    Note: This will fail if users are still assigned to this role.
    """
    RoleService.delete_role(db, role_id)
    return None

@router.get("/{role_id}/permissions", response_model=List[dict])
def get_role_permissions(role_id: int, db: Session = Depends(get_db)):
    """
    Get all permissions assigned to a specific role.
    
    - **role_id**: The ID of the role to get permissions for
    """
    permissions = RoleService.get_role_permissions(db, role_id)
    return [{"permission_id": p.permission_id, "name": p.name, "key": p.key, "description": p.description} for p in permissions]

@router.post("/{role_id}/permissions/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def assign_permission_to_role(role_id: int, permission_id: int, db: Session = Depends(get_db)):
    """
    Assign a permission to a role.
    
    - **role_id**: The ID of the role
    - **permission_id**: The ID of the permission to assign
    """
    RoleService.assign_permission_to_role(db, role_id, permission_id)
    return None

@router.delete("/{role_id}/permissions/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_permission_from_role(role_id: int, permission_id: int, db: Session = Depends(get_db)):
    """
    Remove a permission from a role.
    
    - **role_id**: The ID of the role
    - **permission_id**: The ID of the permission to remove
    """
    RoleService.remove_permission_from_role(db, role_id, permission_id)
    return None
