"""empty message

Revision ID: 9247e5832834
Revises: b385a5574598
Create Date: 2018-12-07 14:22:25.605557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9247e5832834'
down_revision = 'b385a5574598'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('training_session', sa.Column('date_done', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('training_session', 'date_done')
    # ### end Alembic commands ###