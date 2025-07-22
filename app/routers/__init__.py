# app/routers/__init__.py

from .ping import router as ping_router
from .users import router as users_router
from .orders import router as orders_router
from .roles import router as roles_router
from .permissions import router as permissions_router

__all__ = [
    "ping_router",
    "users_router", 
    "orders_router",
    "roles_router",
    "permissions_router"
]
