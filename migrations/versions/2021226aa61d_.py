"""empty message

Revision ID: 2021226aa61d
Revises: 11e5a7247bf9
Create Date: 2017-08-06 13:07:02.478711

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2021226aa61d'
down_revision = '11e5a7247bf9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('training_session',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('training_goal', sa.String(length=60), nullable=True),
    sa.Column('training_type', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('training_session_exercises',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('training_session_id', sa.Integer(), nullable=True),
    sa.Column('training_part', sa.SmallInteger(), nullable=True),
    sa.Column('exercise', sa.Integer(), nullable=True),
    sa.Column('sets', sa.Integer(), nullable=True),
    sa.Column('reps', sa.Integer(), nullable=True),
    sa.Column('weight', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['training_session_id'], ['training_session.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('training_session_exercises')
    op.drop_table('training_session')
    # ### end Alembic commands ###
