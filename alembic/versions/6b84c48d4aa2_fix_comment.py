"""fix comment

Revision ID: 6b84c48d4aa2
Revises: efc41fe41d50
Create Date: 2025-07-26 11:38:06.853229

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b84c48d4aa2'
down_revision: Union[str, Sequence[str], None] = 'efc41fe41d50'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
