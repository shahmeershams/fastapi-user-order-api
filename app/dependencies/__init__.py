# app/dependencies/__init__.py

from .auth import (
    get_current_user,
    get_current_active_user,
    get_current_user_id,
    require_role,
    require_admin,
    require_customer_or_admin,
    require_permission,
    get_user_permissions,
    check_resource_ownership,
    get_optional_current_user
)

__all__ = [
    "get_current_user",
    "get_current_active_user", 
    "get_current_user_id",
    "require_role",
    "require_admin",
    "require_customer_or_admin",
    "require_permission",
    "get_user_permissions", 
    "check_resource_ownership",
    "get_optional_current_user"
]
