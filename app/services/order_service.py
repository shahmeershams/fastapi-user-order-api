# app/services/order_service.py

from sqlalchemy.orm import Session
from app.database.models import Order, User
from app.validators import OrderCreate, OrderUpdate, OrderResponse, OrderListResponse, OrderStatus
from fastapi import HTTPException, status
import uuid

class OrderService:
    @staticmethod
    def create_order(db: Session, order: OrderCreate, user_id: int) -> OrderResponse:
        # Check if user exists
        user = db.query(User).filter_by(user_id=user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        # Generate order code if not provided
        order_code = order.order_code or f"ORD-{uuid.uuid4().hex[:8].upper()}"
        
        # Create new order
        new_order = Order(
            order_code=order_code,
            user_id=user_id,
            total_amount=order.total_amount,
            status=OrderStatus.PENDING
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return OrderResponse.model_validate(new_order)

    @staticmethod
    def get_order(db: Session, order_id: int) -> OrderResponse:
        order = db.query(Order).filter_by(order_id=order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        return OrderResponse.model_validate(order)

    @staticmethod
    def update_order(db: Session, order_id: int, order_update: OrderUpdate) -> OrderResponse:
        order = db.query(Order).filter_by(order_id=order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        
        # Update fields
        if order_update.total_amount is not None:
            order.total_amount = order_update.total_amount
        if order_update.status is not None:
            order.status = order_update.status
        
        db.commit()
        db.refresh(order)
        return OrderResponse.model_validate(order)

    @staticmethod
    def delete_order(db: Session, order_id: int):
        order = db.query(Order).filter_by(order_id=order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        db.delete(order)
        db.commit()

    @staticmethod
    def list_orders(db: Session, page: int = 1, per_page: int = 10) -> OrderListResponse:
        query = db.query(Order)
        total = query.count()
        orders = query.offset((page - 1) * per_page).limit(per_page).all()
        return OrderListResponse(orders=[OrderResponse.model_validate(order) for order in orders], total=total, page=page, per_page=per_page)

    @staticmethod
    def list_user_orders(db: Session, user_id: int, page: int = 1, per_page: int = 10) -> OrderListResponse:
        query = db.query(Order).filter_by(user_id=user_id)
        total = query.count()
        orders = query.offset((page - 1) * per_page).limit(per_page).all()
        return OrderListResponse(orders=[OrderResponse.model_validate(order) for order in orders], total=total, page=page, per_page=per_page)

    @staticmethod
    def update_order_status(db: Session, order_id: int, new_status: OrderStatus) -> OrderResponse:
        order = db.query(Order).filter_by(order_id=order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        
        order.status = new_status
        db.commit()
        db.refresh(order)
        return OrderResponse.model_validate(order)

    @staticmethod
    def check_order_ownership(db: Session, order_id: int, user_id: int) -> bool:
        """Check if an order belongs to a specific user"""
        order = db.query(Order).filter_by(order_id=order_id, user_id=user_id).first()
        return order is not None
