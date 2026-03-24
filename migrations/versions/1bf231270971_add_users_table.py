"""add users table

Revision ID: 1bf231270971
Revises: fd4990dbe8cc
Create Date: 2026-03-19 13:46:13.153639

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1bf231270971'
down_revision = 'fd4990dbe8cc'
branch_labels = None
depends_on = None




def downgrade():
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
