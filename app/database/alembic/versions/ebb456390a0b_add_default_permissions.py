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
    # This migration file previously inserted default permissions data.
    # Data insertion has been moved to the seeder script (seed_database.py)
    # to follow best practices: migrations for schema, seeders for data.
    pass


def downgrade() -> None:
    """Downgrade schema."""
    # No schema changes to revert since data insertion was moved to seeder
    pass
