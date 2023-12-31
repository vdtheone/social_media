"""V_00_10_change_user_mobile_no_field

Revision ID: c497401d69ed
Revises: fa2d37047a18
Create Date: 2023-10-13 21:58:57.804954

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c497401d69ed"
down_revision: Union[str, None] = "fa2d37047a18"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users",
        "mobile_no",
        existing_type=sa.INTEGER(),
        type_=sa.String(),
        existing_nullable=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users",
        "mobile_no",
        existing_type=sa.String(),
        type_=sa.INTEGER(),
        existing_nullable=True,
    )
    # ### end Alembic commands ###
