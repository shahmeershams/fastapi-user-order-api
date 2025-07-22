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
    # This migration file previously inserted role-permission assignment data.
    # Data insertion has been moved to the seeder script (seed_database.py)
    # to follow best practices: migrations for schema, seeders for data.
    pass


def downgrade() -> None:
    """Downgrade schema."""
    # No schema changes to revert since data insertion was moved to seeder
    pass
