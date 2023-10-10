"""V_00_5_Change_image_datatype

Revision ID: 85145e89d339
Revises: d86a1cea94c6
Create Date: 2023-10-09 10:16:31.758752

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "85145e89d339"
down_revision: Union[str, None] = "d86a1cea94c6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "posts",
        "image",
        existing_type=postgresql.BYTEA(),
        type_=sa.String(),
        existing_nullable=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "posts",
        "image",
        existing_type=sa.String(),
        type_=postgresql.BYTEA(),
        existing_nullable=True,
    )
    # ### end Alembic commands ###
