"""Create User Item

Revision ID: 2ac65e6a99d5
Revises: 
Create Date: 2024-03-18 16:03:03.517498

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ac65e6a99d5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(50), nullable=False),
        sa.Column('hashed_password', sa.String(50), nullable=False),
        sa.Column('is_active', sa.Boolean())
    )
    op.create_table(
        'items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(50), nullable=False),
        sa.Column('description', sa.String(50), nullable=False),
    )

def downgrade() -> None:
    op.drop_table("users")
    op.drop_table("items")
