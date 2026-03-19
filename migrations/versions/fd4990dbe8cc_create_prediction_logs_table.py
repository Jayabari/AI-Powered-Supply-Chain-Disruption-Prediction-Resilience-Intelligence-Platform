"""create prediction_logs table

Revision ID: fd4990dbe8cc
Revises: 
Create Date: 2026-03-19 13:30:55.690552

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd4990dbe8cc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'prediction_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('event_type', sa.String(length=100), nullable=False),
        sa.Column('severity_level', sa.String(length=20), nullable=False),
        sa.Column('cause', sa.String(length=120), nullable=False),
        sa.Column('country', sa.String(length=120), nullable=False),
        sa.Column('financial_impact', sa.Float(), nullable=False),
        sa.Column('prediction', sa.Integer(), nullable=False),
        sa.Column('probability', sa.Float(), nullable=False),
        sa.Column('risk_level', sa.String(length=20), nullable=False),
        sa.Column('source', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('prediction_logs')
