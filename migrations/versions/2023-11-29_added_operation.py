"""Added Operation

Revision ID: 456c9eddfdf7
Revises: 8fbe784a3215
Create Date: 2023-11-29 22:47:43.967723

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '456c9eddfdf7'
down_revision: Union[str, None] = '8fbe784a3215'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('operation',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('quantity', sa.String(), nullable=True),
                    sa.Column('figi', sa.String(), nullable=True),
                    sa.Column('instrument_type', sa.String(), nullable=False),
                    sa.Column('date', sa.TIMESTAMP(), nullable=True),
                    sa.Column('type', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('operation')
    # ### end Alembic commands ###