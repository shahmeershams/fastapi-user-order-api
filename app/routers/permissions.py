# app/routers/permissions.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services import PermissionService
from app.validators import PermissionCreate, PermissionUpdate, PermissionResponse, PermissionListResponse

router = APIRouter(prefix="/permissions", tags=["permissions"])

@router.post("/", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED)
def create_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    """
    Create a new permission.
    
    - **name**: Display name for the permission (e.g., "Create User")
    - **key**: Unique identifier for the permission (e.g., "user:create")
    - **description**: Description of what this permission allows
    """
    return PermissionService.create_permission(db, permission)

@router.get("/", response_model=PermissionListResponse)
def list_permissions(db: Session = Depends(get_db)):
    """
    Get all permissions in the system.
    
    Returns a list of all available permissions with their details.
    """
    return PermissionService.list_permissions(db)

@router.get("/{permission_id}", response_model=PermissionResponse)
def get_permission(permission_id: int, db: Session = Depends(get_db)):
    """
    Get a specific permission by ID.
    
    - **permission_id**: The ID of the permission to retrieve
    """
    return PermissionService.get_permission(db, permission_id)

@router.put("/{permission_id}", response_model=PermissionResponse)
def update_permission(permission_id: int, permission_update: PermissionUpdate, db: Session = Depends(get_db)):
    """
    Update a permission's information.
    
    - **permission_id**: The ID of the permission to update
    - **permission_update**: Fields to update (all optional)
    """
    return PermissionService.update_permission(db, permission_id, permission_update)

@router.delete("/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(permission_id: int, db: Session = Depends(get_db)):
    """
    Delete a permission.
    
    - **permission_id**: The ID of the permission to delete
    
    Note: This will fail if the permission is still assigned to any roles.
    """
    PermissionService.delete_permission(db, permission_id)
    return None
