# app/routers/role_permissions.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services import RoleService

router = APIRouter(prefix="/roles/{role_id}/permissions", tags=["role-permissions"])

@router.post("/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def assign_permission_to_role(role_id: int, permission_id: int, db: Session = Depends(get_db)):
    """
    Assign a permission to a role.
    
    - **role_id**: The ID of the role
    - **permission_id**: The ID of the permission to assign
    """
    RoleService.assign_permission_to_role(db, role_id, permission_id)
    return None

@router.delete("/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_permission_from_role(role_id: int, permission_id: int, db: Session = Depends(get_db)):
    """
    Remove a permission from a role.
    
    - **role_id**: The ID of the role
    - **permission_id**: The ID of the permission to remove
    """
    RoleService.remove_permission_from_role(db, role_id, permission_id)
    return None

