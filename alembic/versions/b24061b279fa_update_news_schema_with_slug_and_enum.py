"""update news schema with slug and enum

Revision ID: b24061b279fa
Revises: 8a7b6c5d4e3f
Create Date: 2026-05-04 20:02:45.639181

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b24061b279fa'
down_revision: Union[str, Sequence[str], None] = '8a7b6c5d4e3f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Matches psychohelp.models.news.NewsType member names (SQLAlchemy persists enum names).
_NEWS_TYPE_NAME = 'newstype'


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    # application_audit_logs / applications / appointments changes live in 62e8ab982071.
    # Recover partial runs that created newstype with wrong labels before failing on DROP INDEX.
    op.execute(sa.text(f'DROP TYPE IF EXISTS {_NEWS_TYPE_NAME} CASCADE'))
    postgresql.ENUM('ANNOUNCEMENT', 'REPORT', name=_NEWS_TYPE_NAME).create(bind, checkfirst=False)

    # NOT NULL slug: add nullable, backfill from id, then enforce NOT NULL (existing rows).
    op.add_column(
        'news',
        sa.Column('slug', sa.String(length=255), nullable=True, comment='Уникальный URL'),
    )
    op.execute(
        sa.text("UPDATE news SET slug = REPLACE(id::text, '-', '') WHERE slug IS NULL OR slug = ''")
    )
    op.alter_column('news', 'slug', existing_type=sa.String(length=255), nullable=False)

    op.add_column('news', sa.Column('image', sa.String(length=1024), nullable=True, comment='Ссылка на картинку'))
    op.add_column(
        'news',
        sa.Column(
            'type',
            postgresql.ENUM('ANNOUNCEMENT', 'REPORT', name=_NEWS_TYPE_NAME, create_type=False),
            nullable=True,
            comment='Тип новости',
        ),
    )
    op.add_column(
        'news',
        sa.Column('date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.add_column('news', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('news', sa.Column('link', sa.String(length=1024), nullable=True))
    op.alter_column(
        'news',
        'title',
        existing_type=sa.VARCHAR(length=255),
        comment=None,
        existing_comment='Заголовок новости',
        existing_nullable=False,
    )
    op.alter_column(
        'news',
        'text',
        existing_type=sa.TEXT(),
        nullable=True,
        comment=None,
        existing_comment='Текст новости',
    )
    op.create_index(op.f('ix_news_slug'), 'news', ['slug'], unique=True)
    op.drop_column('news', 'created_at')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        'news',
        sa.Column(
            'created_at',
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            autoincrement=False,
            nullable=False,
            comment='Дата и время создания',
        ),
    )
    op.drop_index(op.f('ix_news_slug'), table_name='news')
    op.alter_column(
        'news',
        'text',
        existing_type=sa.TEXT(),
        nullable=False,
        comment='Текст новости',
    )
    op.alter_column(
        'news',
        'title',
        existing_type=sa.VARCHAR(length=255),
        comment='Заголовок новости',
        existing_nullable=False,
    )
    op.drop_column('news', 'link')
    op.drop_column('news', 'description')
    op.drop_column('news', 'date')
    op.drop_column('news', 'type')
    op.drop_column('news', 'image')
    op.drop_column('news', 'slug')

    postgresql.ENUM('ANNOUNCEMENT', 'REPORT', name=_NEWS_TYPE_NAME).drop(op.get_bind(), checkfirst=True)
