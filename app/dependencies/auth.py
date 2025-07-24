# app/dependencies/auth.py

from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services import AuthService
from app.database.models import User, Role, Permission, RolePermission
from typing import Optional, List
from functools import wraps

# HTTP Bearer token security scheme
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Extract current user from JWT token.
    
    This dependency validates the JWT token and returns the current user.
    Use this for endpoints that require authentication.
    """
    token = credentials.credentials
    return AuthService.get_current_user_from_token(db, token)

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Get current active user (can be extended to check if user is active/enabled).
    
    Currently just returns the user, but can be extended to check user status.
    """
    # Add user active/inactive checks here if needed
    # if not current_user.is_active:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def require_role(allowed_roles: List[str]):
    """
    Create a dependency that requires specific roles.
    
    Usage:
        @router.get("/admin-only")
        def admin_endpoint(user: User = Depends(require_role(["admin"]))):
            ...
    """
    def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role.key not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join(allowed_roles)}"
            )
        return current_user
    return role_checker

def require_admin(current_user: User = Depends(get_current_active_user)) -> User:
    """
    Dependency that requires admin role.
    
    Usage:
        @router.get("/admin-endpoint")
        def admin_only(user: User = Depends(require_admin)):
            ...
    """
    if current_user.role.key != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

def require_customer_or_admin(current_user: User = Depends(get_current_active_user)) -> User:
    """
    Dependency that requires customer or admin role.
    
    Usage:
        @router.get("/customer-endpoint")
        def customer_or_admin(user: User = Depends(require_customer_or_admin)):
            ...
    """
    if current_user.role.key not in ["customer", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Customer or admin access required"
        )
    return current_user

def get_user_permissions(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)) -> List[str]:
    """
    Get current user's permissions.
    
    Returns a list of permission keys that the user has.
    """
    permissions = db.query(Permission.key).join(RolePermission).filter(
        RolePermission.role_id == current_user.role_id
    ).all()
    
    return [perm[0] for perm in permissions]

def require_permission(required_permissions: List[str]):
    """
    Create a dependency that requires specific permissions.
    
    Usage:
        @router.post("/create-user")
        def create_user_endpoint(user: User = Depends(require_permission(["user:create"]))):
            ...
    """
    def permission_checker(
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
    ) -> User:
        user_permissions = get_user_permissions(current_user, db)
        
        # Check if user has any of the required permissions
        has_permission = any(perm in user_permissions for perm in required_permissions)
        
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required permissions: {', '.join(required_permissions)}"
            )
        return current_user
    return permission_checker

def get_current_user_id(current_user: User = Depends(get_current_active_user)) -> int:
    """
    Get current user's ID.
    
    Useful for endpoints that need just the user ID.
    """
    return current_user.user_id

def check_resource_ownership(resource_user_id: int, current_user: User = Depends(get_current_active_user)):
    """
    Check if current user owns the resource or is admin.
    
    This is used to ensure customers can only access their own data.
    Admins can access any resource.
    """
    if current_user.role.key == "admin":
        return True
    
    if current_user.user_id != resource_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. You can only access your own resources."
        )
    
    return True

def get_optional_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Get current user if token is provided, otherwise return None.
    
    Useful for endpoints that work for both authenticated and anonymous users.
    """
    if not authorization or not authorization.startswith("Bearer "):
        return None
    
    token = authorization.split(" ")[1]
    
    try:
        return AuthService.get_current_user_from_token(db, token)
    except HTTPException:
        return None
