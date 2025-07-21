"""Assign default permissions to roles

Revision ID: 7450045c19b9
Revises: ebb456390a0b
Create Date: 2025-07-18 17:07:54.989176

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7450045c19b9'
down_revision: Union[str, Sequence[str], None] = 'ebb456390a0b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Assign permissions to Administrator role (role_id = 1)
    # Admin gets ALL permissions
    admin_permissions = [
        # User Management - Full Access
        1, 2, 3, 4, 5, 6, 7, 8,
        # Order Management - Full Access
        9, 10, 11, 12, 13, 14, 15, 16, 17,
        # Role Management - Full Access
        18, 19, 20, 21, 22, 23,
        # Permission Management - Full Access
        24, 25, 26, 27, 28,
        # Role-Permission Assignment - Full Access
        29, 30
    ]
    
    # Assign permissions to Customer role (role_id = 2)
    # Customer gets LIMITED permissions - only self-management and basic operations
    customer_permissions = [
        # User Management - Own profile only
        6, 7, 8,  # read_own, update_own, delete_own
        # Order Management - Own orders only + create
        9, 14, 15, 16,  # create, read_own, update_own, delete_own
        # Role Management - Read only
        19, 22,  # read, list
        # Permission Management - Read only
        25, 28,  # read, list
    ]
    
    # Insert role-permission assignments for Admin
    for permission_id in admin_permissions:
        op.execute(
            f"INSERT INTO role_permissions (role_id, permission_id) VALUES "
            f"(1, {permission_id})"
        )
    
    # Insert role-permission assignments for Customer
    for permission_id in customer_permissions:
        op.execute(
            f"INSERT INTO role_permissions (role_id, permission_id) VALUES "
            f"(2, {permission_id})"
        )


def downgrade() -> None:
    """Downgrade schema."""
    # Remove all role-permission assignments for default roles
    op.execute("DELETE FROM role_permissions WHERE role_id IN (1, 2)")
