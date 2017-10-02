"""empty message

Revision ID: a1578d56ef16
Revises: 3e67097bcb82
Create Date: 2017-09-26 12:48:19.958327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1578d56ef16'
down_revision = '3e67097bcb82'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exercises', sa.Column('percentage_of_bodyweight', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('exercises', 'percentage_of_bodyweight')
    # ### end Alembic commands ###