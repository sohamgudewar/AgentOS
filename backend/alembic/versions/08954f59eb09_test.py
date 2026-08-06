"""test

Revision ID: 08954f59eb09
Revises: dabd9a2b3707
Create Date: 2026-08-05 18:04:24.306834

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08954f59eb09'
down_revision: Union[str, Sequence[str], None] = 'dabd9a2b3707'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
