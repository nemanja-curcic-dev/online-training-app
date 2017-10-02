"""empty message

Revision ID: 0175705d0574
Revises: 25628002a19d
Create Date: 2017-09-12 10:45:11.798555

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0175705d0574'
down_revision = '25628002a19d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('training_session_exercises', 'weight')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('training_session_exercises', sa.Column('weight', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
