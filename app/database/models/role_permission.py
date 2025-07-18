# app/database/models/role_permission.py

from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.config.database import Base

class RolePermission(Base):
    """
    Role-Permission Junction Table
    
    This model represents the many-to-many relationship between roles and permissions.
    It allows us to assign multiple permissions to a role, and the same permission
    can be assigned to multiple roles.
    """
    __tablename__ = "role_permissions"

    role_permission_id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)
    permission_id = Column(Integer, ForeignKey("permissions.permission_id"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    role = relationship("Role", back_populates="role_permissions")
    permission = relationship("Permission", back_populates="role_permissions")

    def __repr__(self):
        return f"<RolePermission(role_id={self.role_id}, permission_id={self.permission_id})>"
