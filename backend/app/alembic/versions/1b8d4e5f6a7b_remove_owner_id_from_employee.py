"""Remove owner_id from Employee

Revision ID: 1b8d4e5f6a7b
Revises: 0b7c3d4e5f6a
Create Date: 2026-06-16 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes

# revision identifiers, used by Alembic.
revision = '1b8d4e5f6a7b'
down_revision = '0b7c3d4e5f6a'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('employee_owner_id_fkey', 'employee', type_='foreignkey')
    op.drop_column('employee', 'owner_id')


def downgrade():
    op.add_column('employee', sa.Column('owner_id', sa.Uuid(), nullable=False))
    op.create_foreign_key('employee_owner_id_fkey', 'employee', 'user', ['owner_id'], ['id'], ondelete='CASCADE')
