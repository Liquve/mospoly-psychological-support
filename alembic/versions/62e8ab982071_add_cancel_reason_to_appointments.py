"""Add cancel_reason to appointments

Revision ID: 62e8ab982071
Revises: c1d2e3f4a5b6
Create Date: 2024-04-12 15:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '62e8ab982071'
down_revision: Union[str, Sequence[str], None] = 'c1d2e3f4a5b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Оставляем ТОЛЬКО добавление колонки cancel_reason
    op.add_column('appointments', sa.Column('cancel_reason', sa.String(length=512), nullable=True, comment='Причина отмены'))


def downgrade() -> None:
    """Downgrade schema."""
    # Оставляем ТОЛЬКО откат добавления колонки cancel_reason
    op.drop_column('appointments', 'cancel_reason')