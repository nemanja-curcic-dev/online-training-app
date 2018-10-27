"""empty message

Revision ID: 63a3cb004c4f
Revises: dfd7378207e6
Create Date: 2018-10-24 12:25:33.670890

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '63a3cb004c4f'
down_revision = 'dfd7378207e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tests', 'result')
    op.drop_column('tests', 'done_timestamp')
    op.add_column('users_tests', sa.Column('done_timestamp', sa.Integer(), nullable=True))
    op.add_column('users_tests', sa.Column('result', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users_tests', 'result')
    op.drop_column('users_tests', 'done_timestamp')
    op.add_column('tests', sa.Column('done_timestamp', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('tests', sa.Column('result', mysql.VARCHAR(length=50), nullable=True))
    # ### end Alembic commands ###
