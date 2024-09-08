"""initial commit

Revision ID: 83b99c010a9e
Revises: 983916be35da
Create Date: 2024-09-08 20:36:57.143244

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '83b99c010a9e'
down_revision: Union[str, None] = '983916be35da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_name', sa.String(), nullable=True))
    op.create_unique_constraint(None, 'users', ['last_name'])
    op.create_unique_constraint(None, 'users', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'last_name')
    # ### end Alembic commands ###