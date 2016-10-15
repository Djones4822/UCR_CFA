"""Rename geom column to geo (geography)

Revision ID: 57ab83bcb2ba
Revises: 7d28b515fd64
Create Date: 2016-09-30 03:48:53.414957

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '57ab83bcb2ba'
down_revision = '7d28b515fd64'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('locations', 'geom', new_column_name='geo')


def downgrade():
    op.alter_column('locations', 'geo', new_column_name='geom')
