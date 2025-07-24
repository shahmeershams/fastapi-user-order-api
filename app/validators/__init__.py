# app/validators/__init__.py

# Import all validators to make them available
from .user import (
    UserBase, UserCreate, UserLogin, UserUpdate, UserResponse,
    UserWithOrdersResponse, UserProfileResponse, UserListResponse
)
from .auth import (
    TokenResponse, RefreshTokenRequest, LogoutRequest, CurrentUserResponse,
    PasswordChangeRequest, PasswordResetRequest, TokenValidationResponse
)
from .role import (
    RoleBase, RoleCreate, RoleUpdate, RoleResponse,
    RoleWithPermissionsResponse, RoleListResponse
)
from .permission import (
    PermissionBase, PermissionCreate, PermissionUpdate, PermissionResponse,
    PermissionListResponse
)
from .order import (
    OrderStatus, OrderBase, OrderCreate, OrderUpdate, OrderResponse,
    OrderWithUserResponse, OrderListResponse, OrderStatusUpdate
)
# Auth validators now included

__all__ = [
    # User models
    "UserBase", "UserCreate", "UserLogin", "UserUpdate", "UserResponse",
    "UserWithOrdersResponse", "UserProfileResponse", "UserListResponse",
    
    # Auth models
    "TokenResponse", "RefreshTokenRequest", "LogoutRequest", "CurrentUserResponse",
    "PasswordChangeRequest", "PasswordResetRequest", "TokenValidationResponse",
    
    # Role models
    "RoleBase", "RoleCreate", "RoleUpdate", "RoleResponse",
    "RoleWithPermissionsResponse", "RoleListResponse",
    
    # Permission models
    "PermissionBase", "PermissionCreate", "PermissionUpdate", "PermissionResponse",
    "PermissionListResponse",
    
    # Order models
    "OrderStatus", "OrderBase", "OrderCreate", "OrderUpdate", "OrderResponse",
    "OrderWithUserResponse", "OrderListResponse", "OrderStatusUpdate",
    
]
