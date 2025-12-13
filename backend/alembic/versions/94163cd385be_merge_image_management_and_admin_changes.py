"""merge image management and admin changes

Revision ID: 94163cd385be
Revises: 8f9e5b2c3d4a, d06ebaf6a6a6
Create Date: 2025-12-09 10:41:38.732290

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94163cd385be'
down_revision: Union[str, Sequence[str], None] = ('8f9e5b2c3d4a', 'd06ebaf6a6a6')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
