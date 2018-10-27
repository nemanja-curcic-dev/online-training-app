"""empty message

Revision ID: dfd7378207e6
Revises: d279b9e6985c
Create Date: 2018-10-24 11:18:04.118231

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfd7378207e6'
down_revision = 'd279b9e6985c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('test_name', sa.String(length=100), nullable=True),
    sa.Column('test_category', sa.String(length=64), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('result', sa.String(length=50), nullable=True),
    sa.Column('img_url', sa.String(length=64), nullable=True),
    sa.Column('video_url', sa.String(length=256), nullable=True),
    sa.Column('done_timestamp', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_tests',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('test_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['test_id'], ['tests.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.add_column('users', sa.Column('first_time', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'first_time')
    op.drop_table('users_tests')
    op.drop_table('tests')
    # ### end Alembic commands ###