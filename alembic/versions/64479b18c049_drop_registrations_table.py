"""drop registrations table

Revision ID: 64479b18c049
Revises: 6186bf412637
Create Date: 2026-02-26 12:06:08.442016

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64479b18c049'
down_revision: Union[str, Sequence[str], None] = '6186bf412637'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
