"""empty message

Revision ID: f956ffc2dd3a
Revises: e14bc9307c90
Create Date: 2017-09-12 11:13:01.691690

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f956ffc2dd3a'
down_revision = 'e14bc9307c90'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('has_new_training', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'has_new_training')
    # ### end Alembic commands ###