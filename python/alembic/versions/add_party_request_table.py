"""add party request table

Revision ID: add_party_request
Revises: e3b646493c91
Create Date: 2025-10-09 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime
import datetime as dt

# revision identifiers, used by Alembic.
revision = 'add_party_request'
down_revision = 'e3b646493c91'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'partyrequest',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('party_id', sa.Integer(), nullable=False),
        sa.Column('accepted', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.ForeignKeyConstraint(['party_id'], ['party.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('partyrequest')

