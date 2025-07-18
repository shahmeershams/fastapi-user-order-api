# app/database/models/user.py

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from app.config.database import Base

class User(Base):
    """
    User Model
    
    This model represents users in the system with Role-Based Access Control (RBAC).
    Each user is assigned a role which determines their permissions.
    """
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    role = relationship("Role", back_populates="users")
    orders = relationship("Order", back_populates="user")
    authenticate_tokens = relationship("AuthenticateToken", back_populates="user")

    def __repr__(self):
        return f"<User(user_id={self.user_id}, username='{self.username}', email='{self.email}')>"
