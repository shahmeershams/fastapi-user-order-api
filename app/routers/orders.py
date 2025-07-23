# app/routers/orders.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services import OrderService
from app.validators import OrderCreate, OrderUpdate, OrderResponse, OrderListResponse, OrderStatusUpdate
from typing import List

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, user_id: int, db: Session = Depends(get_db)):
    """Create a new order for a user"""
    return OrderService.create_order(db, order, user_id)

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get order by ID"""
    return OrderService.get_order(db, order_id)

@router.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    """Update order by ID"""
    return OrderService.update_order(db, order_id, order_update)

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """Delete order by ID"""
    OrderService.delete_order(db, order_id)
    return None

@router.get("/", response_model=OrderListResponse)
def list_orders(page: int = 1, per_page: int = 10, db: Session = Depends(get_db)):
    """List all orders with pagination"""
    return OrderService.list_orders(db, page, per_page)

@router.get("/user/{user_id}", response_model=OrderListResponse)
def list_user_orders(user_id: int, page: int = 1, per_page: int = 10, db: Session = Depends(get_db)):
    """List orders for a specific user"""
    return OrderService.list_user_orders(db, user_id, page, per_page)

@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(order_id: int, status_update: OrderStatusUpdate, db: Session = Depends(get_db)):
    """Update order status"""
    return OrderService.update_order_status(db, order_id, status_update.status)
