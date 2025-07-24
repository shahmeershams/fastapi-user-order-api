# app/routers/orders.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services import OrderService
from app.validators import OrderCreate, OrderUpdate, OrderResponse, OrderListResponse, OrderStatusUpdate
from app.dependencies import (
    get_current_active_user, require_admin, require_customer_or_admin,
    get_current_user_id
)
from app.database.models import User
from typing import List

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order: OrderCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_customer_or_admin)
):
    """
    Create a new order.
    
    - Customers can create orders for themselves
    - Admins can create orders for any user (must specify user_id in request body)
    """
    # For customers, always create order for themselves
    # For admins, they need to specify user_id in the order data or it defaults to them
    user_id = current_user.user_id  # Default to current user
    
    return OrderService.create_order(db, order, user_id)

@router.get("/me", response_model=OrderListResponse)
def get_my_orders(
    page: int = 1,
    per_page: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user's orders.
    
    Returns orders belonging to the currently authenticated user.
    """
    return OrderService.list_user_orders(db, current_user.user_id, page, per_page)

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get order by ID.
    
    - Admins can view any order
    - Customers can only view their own orders
    """
    order = OrderService.get_order(db, order_id)
    
    # Check ownership for customers
    if current_user.role.key != "admin" and order.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. You can only view your own orders."
        )
    
    return order

@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int, 
    order_update: OrderUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update order by ID.
    
    - Admins can update any order
    - Customers can only update their own orders
    """
    # First get the order to check ownership
    order = OrderService.get_order(db, order_id)
    
    # Check ownership for customers
    if current_user.role.key != "admin" and order.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. You can only update your own orders."
        )
    
    return OrderService.update_order(db, order_id, order_update)

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete order by ID.
    
    - Admins can delete any order
    - Customers can only delete their own orders
    """
    # First get the order to check ownership
    order = OrderService.get_order(db, order_id)
    
    # Check ownership for customers
    if current_user.role.key != "admin" and order.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. You can only delete your own orders."
        )
    
    OrderService.delete_order(db, order_id)
    return None

@router.get("/", response_model=OrderListResponse)
def list_orders(
    page: int = 1, 
    per_page: int = 10, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    List orders with pagination.
    
    - Admins can view all orders
    - Customers can only view their own orders
    """
    if current_user.role.key == "admin":
        # Admin can see all orders
        return OrderService.list_orders(db, page, per_page)
    else:
        # Customer can only see their own orders
        return OrderService.list_user_orders(db, current_user.user_id, page, per_page)

@router.get("/user/{user_id}", response_model=OrderListResponse)
def list_user_orders(
    user_id: int, 
    page: int = 1, 
    per_page: int = 10, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    List orders for a specific user.
    
    - Admins can view orders for any user
    - Customers can only view their own orders
    """
    # Check if user can access this resource
    if current_user.role.key != "admin" and current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. You can only view your own orders."
        )
    
    return OrderService.list_user_orders(db, user_id, page, per_page)

@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int, 
    status_update: OrderStatusUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Update order status (Admin only).
    
    Only administrators can update order status.
    """
    return OrderService.update_order_status(db, order_id, status_update.status)

