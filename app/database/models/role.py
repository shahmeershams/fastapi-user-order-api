# app/database/models/role.py

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.config.database import Base

class Role(Base):
    """
    Role Model for Role-Based Access Control (RBAC)
    
    This model represents user roles in the system (e.g., admin, customer).
    Each role has specific permissions that define what actions users can perform.
    """
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)  # Display name like "Administrator"
    key = Column(String(255), unique=True, nullable=False)  # Unique key like "admin"
    description = Column(Text, nullable=False)  # Description of the role
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    users = relationship("User", back_populates="role")
    role_permissions = relationship("RolePermission", back_populates="role")

    def __repr__(self):
        return f"<Role(role_id={self.role_id}, name='{self.name}', key='{self.key}')>"
