# app/database/models/__init__.py

# Import all models here to ensure they are registered with SQLAlchemy
from .user import User
from .order import Order
from .role import Role
from .permission import Permission
from .role_permission import RolePermission
from .authenticate_token import AuthenticateToken

__all__ = [
    "User",
    "Order",
    "Role",
    "Permission",
    "RolePermission",
    "AuthenticateToken",
]
