"""empty message

Revision ID: 25628002a19d
Revises: 2734c5a64fef
Create Date: 2017-09-12 10:32:33.348050

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25628002a19d'
down_revision = '2734c5a64fef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('training_session_muscle_groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('training_session_id', sa.Integer(), nullable=True),
    sa.Column('muscle_group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['training_session_id'], ['training_session.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('training_session_muscle_groups')
    # ### end Alembic commands ###
