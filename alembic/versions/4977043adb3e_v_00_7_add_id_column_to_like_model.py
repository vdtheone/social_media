"""V_00_7_add id column to Like model

Revision ID: 4977043adb3e
Revises: 7765b856562e
Create Date: 2023-10-09 12:50:43.229764

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4977043adb3e"
down_revision: Union[str, None] = "7765b856562e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("likes", sa.Column("id", sa.Integer(), nullable=False))
    op.create_index(op.f("ix_likes_id"), "likes", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_likes_id"), table_name="likes")
    op.drop_column("likes", "id")
    # ### end Alembic commands ###
