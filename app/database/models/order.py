# app/database/models/order.py

from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, Numeric, String, func, Enum
from sqlalchemy.orm import relationship
from app.config.database import Base
from app.validators.order import OrderStatus

class Order(Base):
    """
    Order Model
    
    This model represents customer orders in the system.
    Each order belongs to a user and has a status that tracks its progress.
    """
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    order_code = Column(String(255), unique=True, nullable=False)  # External order identifier
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    order_date = Column(TIMESTAMP, server_default=func.now())
    total_amount = Column(Numeric(10, 2), nullable=False)  # Decimal with 2 decimal places
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="orders")

    def __repr__(self):
        return f"<Order(order_id={self.order_id}, order_code='{self.order_code}', user_id={self.user_id}, status='{self.status}')>"
