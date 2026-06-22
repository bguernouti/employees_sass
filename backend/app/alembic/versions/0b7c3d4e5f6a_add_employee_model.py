"""Add Employee model

Revision ID: 0b7c3d4e5f6a
Revises: fe56fa70289e
Create Date: 2026-06-15 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
import uuid
from datetime import datetime, timezone

# revision identifiers, used by Alembic.
revision = '0b7c3d4e5f6a'
down_revision = 'fe56fa70289e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'employee',
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('position', sa.String(length=255), nullable=True),
        sa.Column('department', sa.String(length=255), nullable=True),
        sa.Column('hire_date', sa.DateTime(), nullable=True),
        sa.Column('salary', sa.Float(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
        sa.Column('owner_id', sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_employee_email'), 'employee', ['email'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_employee_email'), table_name='employee')
    op.drop_table('employee')
