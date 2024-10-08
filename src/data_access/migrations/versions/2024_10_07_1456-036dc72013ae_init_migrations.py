"""init migrations

Revision ID: 036dc72013ae
Revises:
Create Date: 2024-10-07 14:56:35.896979

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '036dc72013ae'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_user')),
        sa.UniqueConstraint('email', name=op.f('uq_user_email')),
        sa.UniqueConstraint('id', name=op.f('uq_user_id')),
        sa.UniqueConstraint('last_name', name=op.f('uq_user_last_name')),
    )
    op.create_table(
        'workspace',
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('owner_id', sa.UUID(), nullable=False),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['user.id'], name=op.f('fk_workspace_owner_id_user')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_workspace')),
        sa.UniqueConstraint('id', name=op.f('uq_workspace_id')),
    )
    op.create_table(
        'category',
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('workspace_id', sa.Integer(), nullable=False),
        sa.Column('owner_id', sa.UUID(), nullable=False),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['user.id'], name=op.f('fk_category_owner_id_user')),
        sa.ForeignKeyConstraint(
            ['workspace_id'], ['workspace.id'], name=op.f('fk_category_workspace_id_workspace')
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_category')),
        sa.UniqueConstraint('id', name=op.f('uq_category_id')),
    )
    op.create_table(
        'meet',
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('meet_at', sa.DateTime(), nullable=False),
        sa.Column('workspace_id', sa.Integer(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('owner_id', sa.UUID(), nullable=False),
        sa.Column('assigned_to', sa.UUID(), nullable=False),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(
            ['assigned_to'], ['user.id'], name=op.f('fk_meet_assigned_to_user')
        ),
        sa.ForeignKeyConstraint(
            ['category_id'], ['category.id'], name=op.f('fk_meet_category_id_category')
        ),
        sa.ForeignKeyConstraint(['owner_id'], ['user.id'], name=op.f('fk_meet_owner_id_user')),
        sa.ForeignKeyConstraint(
            ['workspace_id'], ['workspace.id'], name=op.f('fk_meet_workspace_id_workspace')
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_meet')),
        sa.UniqueConstraint('id', name=op.f('uq_meet_id')),
    )
    op.create_table(
        'participant',
        sa.Column('meet_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['meet_id'], ['meet.id'], name=op.f('fk_participant_meet_id_meet')),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_participant_user_id_user')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_participant')),
        sa.UniqueConstraint('id', name=op.f('uq_participant_id')),
        sa.UniqueConstraint('meet_id', 'user_id', name=op.f('uq_participant_meet_id_user_id')),
    )


def downgrade() -> None:
    op.drop_table('participant')
    op.drop_table('meet')
    op.drop_table('category')
    op.drop_table('workspace')
    op.drop_table('user')
