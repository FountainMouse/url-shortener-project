"""Create URL table

Revision ID: a005d060b88d
Revises: 
Create Date: 2025-12-12 20:40:27.811136

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a005d060b88d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# ... boilerplate code ...

def upgrade():
    op.create_table(
        'urls',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True, index=True),
        sa.Column('original_url', sa.String(), nullable=False),
        sa.Column('short_code', sa.String(length=10), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.UniqueConstraint('short_code', name='uq_urls_short_code') 
    )


def downgrade():
    op.drop_table('urls')
