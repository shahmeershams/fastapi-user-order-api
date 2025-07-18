# app/validators/order.py

from enum import Enum

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
