# app/models/order.py

from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, Numeric, String, func
from app.config.database import Base

class Order(Base):
    __tablename__ = "orders"  # This will be the table name in PostgreSQL

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # Link to users table
    order_date = Column(TIMESTAMP, server_default=func.now())
    total_amount = Column(Numeric, nullable=False)
    status = Column(String(50), default="pending")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
