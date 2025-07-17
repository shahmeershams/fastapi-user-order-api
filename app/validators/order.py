# app/validators/order.py

from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class OrderStatus(str, Enum):
    """
    Order Status Enum
    
    This enum defines the possible states of an order:
    - pending: Order has been placed but not yet processed
    - in_process: Order is currently being processed
    - completed: Order has been successfully completed
    - cancelled: Order has been cancelled
    """
    PENDING = "pending"
    IN_PROCESS = "in_process"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class OrderBase(BaseModel):
    """Base Order model with common fields"""
    total_amount: Decimal = Field(..., gt=0, description="Order total amount must be greater than 0")

class OrderCreate(OrderBase):
    """Order creation model"""
    order_code: Optional[str] = Field(None, max_length=255, description="External order identifier")
    # user_id will be extracted from JWT token, not from request body

class OrderUpdate(BaseModel):
    """Order update model - all fields optional"""
    total_amount: Optional[Decimal] = Field(None, gt=0)
    status: Optional[OrderStatus] = Field(None, description="Order status")

class OrderResponse(OrderBase):
    """Order response model"""
    model_config = ConfigDict(from_attributes=True)
    
    order_id: int
    order_code: str
    user_id: int
    order_date: datetime
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

class OrderWithUserResponse(OrderResponse):
    """Order response with user information"""
    user: Optional['UserResponse'] = None

class OrderListResponse(BaseModel):
    """Response model for order list"""
    orders: List[OrderResponse]
    total: int
    page: int
    per_page: int

class OrderStatusUpdate(BaseModel):
    """Model for updating only order status"""
    status: OrderStatus = Field(..., description="New order status")
