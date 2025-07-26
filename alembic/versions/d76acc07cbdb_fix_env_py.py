"""fix env.py

Revision ID: d76acc07cbdb
Revises: 6b84c48d4aa2
Create Date: 2025-07-26 11:38:52.890212

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd76acc07cbdb'
down_revision: Union[str, Sequence[str], None] = '6b84c48d4aa2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
