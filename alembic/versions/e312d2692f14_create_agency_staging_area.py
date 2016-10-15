"""create agency staging area

Revision ID: e312d2692f14
Revises: 57ab83bcb2ba
Create Date: 2016-10-15 13:38:16.495217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e312d2692f14'
down_revision = '57ab83bcb2ba'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('agency_staging',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('info', sa.dialects.postgresql.JSON))


def downgrade():
    op.drop_table('agency_staging')
