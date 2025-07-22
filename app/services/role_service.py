# app/services/role_service.py

from sqlalchemy.orm import Session
from app.database.models import Role, Permission, RolePermission
from app.validators import RoleCreate, RoleUpdate, RoleResponse, RoleListResponse
from app.validators import PermissionResponse
from fastapi import HTTPException, status

class RoleService:
    @staticmethod
    def create_role(db: Session, role: RoleCreate) -> RoleResponse:
        # Check if role key already exists
        existing_role = db.query(Role).filter_by(key=role.key).first()
        if existing_role:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role key already exists")
        
        new_role = Role(
            name=role.name,
            key=role.key,
            description=role.description
        )
        db.add(new_role)
        db.commit()
        db.refresh(new_role)
        return RoleResponse.model_validate(new_role)

    @staticmethod
    def get_role(db: Session, role_id: int) -> RoleResponse:
        role = db.query(Role).filter_by(role_id=role_id).first()
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
        return RoleResponse.model_validate(role)

    @staticmethod
    def get_role_by_key(db: Session, key: str) -> RoleResponse:
        role = db.query(Role).filter_by(key=key).first()
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
        return RoleResponse.model_validate(role)

    @staticmethod
    def update_role(db: Session, role_id: int, role_update: RoleUpdate) -> RoleResponse:
        role = db.query(Role).filter_by(role_id=role_id).first()
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
        
        # Update fields
        if role_update.name:
            role.name = role_update.name
        if role_update.key:
            role.key = role_update.key
        if role_update.description:
            role.description = role_update.description
        
        db.commit()
        db.refresh(role)
        return RoleResponse.model_validate(role)

    @staticmethod
    def delete_role(db: Session, role_id: int):
        role = db.query(Role).filter_by(role_id=role_id).first()
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
        db.delete(role)
        db.commit()

    @staticmethod
    def list_roles(db: Session) -> RoleListResponse:
        roles = db.query(Role).all()
        return RoleListResponse(roles=[RoleResponse.model_validate(role) for role in roles], total=len(roles))

    @staticmethod
    def assign_permission_to_role(db: Session, role_id: int, permission_id: int):
        # Check if role exists
        role = db.query(Role).filter_by(role_id=role_id).first()
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
        
        # Check if permission exists
        permission = db.query(Permission).filter_by(permission_id=permission_id).first()
        if not permission:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
        
        # Check if permission already assigned
        existing_assignment = db.query(RolePermission).filter_by(
            role_id=role_id, 
            permission_id=permission_id
        ).first()
        if existing_assignment:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permission already assigned to role")
        
        # Assign permission to role
        role_permission = RolePermission(role_id=role_id, permission_id=permission_id)
        db.add(role_permission)
        db.commit()

    @staticmethod
    def remove_permission_from_role(db: Session, role_id: int, permission_id: int):
        role_permission = db.query(RolePermission).filter_by(
            role_id=role_id, 
            permission_id=permission_id
        ).first()
        if not role_permission:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not assigned to role")
        
        db.delete(role_permission)
        db.commit()

    @staticmethod
    def get_role_permissions(db: Session, role_id: int) -> list[PermissionResponse]:
        role = db.query(Role).filter_by(role_id=role_id).first()
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
        
        permissions = db.query(Permission).join(RolePermission).filter(
            RolePermission.role_id == role_id
        ).all()
        
        return [PermissionResponse.model_validate(permission) for permission in permissions]
