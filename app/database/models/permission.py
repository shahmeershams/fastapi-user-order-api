# app/database/models/permission.py

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.config.database import Base

class Permission(Base):
    """
    Permission Model for Role-Based Access Control (RBAC)
    
    This model represents specific permissions that can be granted to roles.
    Examples: 'create_user', 'read_all_orders', 'update_own_profile', etc.
    """
    __tablename__ = "permissions"

    permission_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)  # Display name like "Create User"
    key = Column(String(255), unique=True, nullable=False)  # Unique key like "create_user"
    description = Column(Text, nullable=False)  # Description of what this permission allows
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    role_permissions = relationship("RolePermission", back_populates="permission")

    def __repr__(self):
        return f"<Permission(permission_id={self.permission_id}, name='{self.name}', key='{self.key}')>"
