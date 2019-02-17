"""empty message

Revision ID: c8e62fae9519
Revises: f4133827ef9d
Create Date: 2018-12-19 22:37:16.386511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8e62fae9519'
down_revision = 'f4133827ef9d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('anthropometry_tests', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'anthropometry_tests', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'anthropometry_tests', type_='foreignkey')
    op.drop_column('anthropometry_tests', 'user_id')
    # ### end Alembic commands ###