"""Add default permissions

Revision ID: ebb456390a0b
Revises: 98965b3aa26a
Create Date: 2025-07-18 17:05:56.709728

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ebb456390a0b'
down_revision: Union[str, Sequence[str], None] = '98965b3aa26a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Insert default permissions for the API
    permissions_data = [
        # User Management Permissions
        (1, 'Create User', 'user:create', 'Create new users in the system'),
        (2, 'Read User', 'user:read', 'View user information'),
        (3, 'Update User', 'user:update', 'Update user information'),
        (4, 'Delete User', 'user:delete', 'Delete users from the system'),
        (5, 'List Users', 'user:list', 'List all users in the system'),
        (6, 'Read Own Profile', 'user:read_own', 'View own user profile'),
        (7, 'Update Own Profile', 'user:update_own', 'Update own user profile'),
        (8, 'Delete Own Account', 'user:delete_own', 'Delete own user account'),
        
        # Order Management Permissions
        (9, 'Create Order', 'order:create', 'Create new orders'),
        (10, 'Read Order', 'order:read', 'View order information'),
        (11, 'Update Order', 'order:update', 'Update order information'),
        (12, 'Delete Order', 'order:delete', 'Delete orders'),
        (13, 'List Orders', 'order:list', 'List all orders in the system'),
        (14, 'Read Own Orders', 'order:read_own', 'View own orders'),
        (15, 'Update Own Orders', 'order:update_own', 'Update own orders'),
        (16, 'Delete Own Orders', 'order:delete_own', 'Delete own orders'),
        (17, 'Update Order Status', 'order:update_status', 'Update order status'),
        
        # Role Management Permissions
        (18, 'Create Role', 'role:create', 'Create new roles'),
        (19, 'Read Role', 'role:read', 'View role information'),
        (20, 'Update Role', 'role:update', 'Update role information'),
        (21, 'Delete Role', 'role:delete', 'Delete roles'),
        (22, 'List Roles', 'role:list', 'List all roles in the system'),
        (23, 'Read Role Permissions', 'role:read_permissions', 'View permissions assigned to roles'),
        
        # Permission Management Permissions
        (24, 'Create Permission', 'permission:create', 'Create new permissions'),
        (25, 'Read Permission', 'permission:read', 'View permission information'),
        (26, 'Update Permission', 'permission:update', 'Update permission information'),
        (27, 'Delete Permission', 'permission:delete', 'Delete permissions'),
        (28, 'List Permissions', 'permission:list', 'List all permissions in the system'),
        
        # Role-Permission Assignment Permissions
        (29, 'Assign Permission to Role', 'role_permission:assign', 'Assign permissions to roles'),
        (30, 'Remove Permission from Role', 'role_permission:remove', 'Remove permissions from roles'),
    ]
    
    # Insert all permissions
    for permission_id, name, key, description in permissions_data:
        op.execute(
            f"INSERT INTO permissions (permission_id, name, `key`, description) VALUES "
            f"({permission_id}, '{name}', '{key}', '{description}')"
        )


def downgrade() -> None:
    """Downgrade schema."""
    # Remove all default permissions
    permission_keys = [
        'user:create', 'user:read', 'user:update', 'user:delete', 'user:list',
        'user:read_own', 'user:update_own', 'user:delete_own',
        'order:create', 'order:read', 'order:update', 'order:delete', 'order:list',
        'order:read_own', 'order:update_own', 'order:delete_own', 'order:update_status',
        'role:create', 'role:read', 'role:update', 'role:delete', 'role:list', 'role:read_permissions',
        'permission:create', 'permission:read', 'permission:update', 'permission:delete', 'permission:list',
        'role_permission:assign', 'role_permission:remove'
    ]
    
    keys_str = "', '".join(permission_keys)
    op.execute(f"DELETE FROM permissions WHERE `key` IN ('{keys_str}')")
