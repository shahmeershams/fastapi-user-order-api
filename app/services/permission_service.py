# app/services/permission_service.py

from sqlalchemy.orm import Session
from app.database.models import Permission
from app.validators import PermissionCreate, PermissionUpdate, PermissionResponse, PermissionListResponse
from fastapi import HTTPException, status

class PermissionService:
    @staticmethod
    def create_permission(db: Session, permission: PermissionCreate) -> PermissionResponse:
        # Check if permission key already exists
        existing_permission = db.query(Permission).filter_by(key=permission.key).first()
        if existing_permission:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permission key already exists")
        
        new_permission = Permission(
            name=permission.name,
            key=permission.key,
            description=permission.description
        )
        db.add(new_permission)
        db.commit()
        db.refresh(new_permission)
        return PermissionResponse.model_validate(new_permission)

    @staticmethod
    def get_permission(db: Session, permission_id: int) -> PermissionResponse:
        permission = db.query(Permission).filter_by(permission_id=permission_id).first()
        if not permission:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
        return PermissionResponse.model_validate(permission)

    @staticmethod
    def update_permission(db: Session, permission_id: int, permission_update: PermissionUpdate) -> PermissionResponse:
        permission = db.query(Permission).filter_by(permission_id=permission_id).first()
        if not permission:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
        
        # Update fields
        if permission_update.name:
            permission.name = permission_update.name
        if permission_update.key:
            permission.key = permission_update.key
        if permission_update.description:
            permission.description = permission_update.description
        
        db.commit()
        db.refresh(permission)
        return PermissionResponse.model_validate(permission)

    @staticmethod
    def delete_permission(db: Session, permission_id: int):
        permission = db.query(Permission).filter_by(permission_id=permission_id).first()
        if not permission:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
        db.delete(permission)
        db.commit()

    @staticmethod
    def list_permissions(db: Session) -> PermissionListResponse:
        permissions = db.query(Permission).all()
        return PermissionListResponse(permissions=[PermissionResponse.model_validate(permission) for permission in permissions], total=len(permissions))
