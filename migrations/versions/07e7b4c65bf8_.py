"""empty message

Revision ID: 07e7b4c65bf8
Revises: f956ffc2dd3a
Create Date: 2017-09-13 10:27:29.024388

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07e7b4c65bf8'
down_revision = 'f956ffc2dd3a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exercises', sa.Column('variation_of', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('exercises', 'variation_of')
    # ### end Alembic commands ###
