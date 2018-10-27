"""empty message

Revision ID: 09c9c2ce0aab
Revises: 63a3cb004c4f
Create Date: 2018-10-24 12:30:00.603674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09c9c2ce0aab'
down_revision = '63a3cb004c4f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tests', sa.Column('alone', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tests', 'alone')
    # ### end Alembic commands ###