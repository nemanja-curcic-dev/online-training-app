"""empty message

Revision ID: c7817ddb3c5b
Revises: 79a94a3f7d84
Create Date: 2018-12-19 12:46:12.893486

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7817ddb3c5b'
down_revision = '79a94a3f7d84'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('anthropometry_users_tests', sa.Column('vinjak_mass', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('anthropometry_users_tests', 'vinjak_mass')
    # ### end Alembic commands ###
