# main.py

from fastapi import FastAPI
from app.routers import (
    ping_router, 
    users_router, 
    orders_router,
    roles_router,
    permissions_router,
    role_permissions_router
)

app = FastAPI(
    title="User Order API",
    description="A RESTful API for managing users and orders with Role-Based Access Control",
    version="1.0.0"
)

# Register all routers
app.include_router(ping_router)
app.include_router(users_router)
app.include_router(orders_router)
app.include_router(roles_router)
app.include_router(permissions_router)
app.include_router(role_permissions_router)



