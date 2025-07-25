"""Add default roles data

Revision ID: 98965b3aa26a
Revises: ca1ed7b81174
Create Date: 2025-07-16 15:53:42.665230

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '98965b3aa26a'
down_revision: Union[str, Sequence[str], None] = 'ca1ed7b81174'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    
    # This migration file previously inserted default role data.
    # Data insertion has been moved to the seeder script (seed_database.py)
    # to follow best practices: migrations for schema, seeders for data.
    pass
    
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    
    # No schema changes to revert since data insertion was moved to seeder
    pass
    
    # ### end Alembic commands ###
