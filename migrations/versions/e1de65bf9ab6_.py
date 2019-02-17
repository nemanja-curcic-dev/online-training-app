"""empty message

Revision ID: e1de65bf9ab6
Revises: e798041ebc6f
Create Date: 2018-12-19 12:10:40.843522

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e1de65bf9ab6'
down_revision = 'e798041ebc6f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tests', 'img_url')
    op.drop_column('tests', 'video_url')
    op.drop_column('tests', 'short_name')
    op.drop_column('tests', 'alone')
    op.drop_column('tests', 'description')
    op.drop_column('tests', 'unit')
    op.add_column('users_tests', sa.Column('body_fat_mass', sa.Integer(), nullable=True))
    op.add_column('users_tests', sa.Column('body_fat_percentage', sa.Integer(), nullable=True))
    op.add_column('users_tests', sa.Column('muscle_mass', sa.Integer(), nullable=True))
    op.add_column('users_tests', sa.Column('muscle_mass_percentage', sa.Integer(), nullable=True))
    op.add_column('users_tests', sa.Column('thigh', sa.Integer(), nullable=True))
    op.add_column('users_tests', sa.Column('waist', sa.Integer(), nullable=True))
    op.add_column('users_tests', sa.Column('weight', sa.Integer(), nullable=True))
    op.drop_column('users_tests', 'result')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users_tests', sa.Column('result', mysql.VARCHAR(length=50), nullable=True))
    op.drop_column('users_tests', 'weight')
    op.drop_column('users_tests', 'waist')
    op.drop_column('users_tests', 'thigh')
    op.drop_column('users_tests', 'muscle_mass_percentage')
    op.drop_column('users_tests', 'muscle_mass')
    op.drop_column('users_tests', 'body_fat_percentage')
    op.drop_column('users_tests', 'body_fat_mass')
    op.add_column('tests', sa.Column('unit', mysql.VARCHAR(length=20), nullable=True))
    op.add_column('tests', sa.Column('description', mysql.TEXT(), nullable=True))
    op.add_column('tests', sa.Column('alone', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.add_column('tests', sa.Column('short_name', mysql.VARCHAR(length=30), nullable=True))
    op.add_column('tests', sa.Column('video_url', mysql.VARCHAR(length=256), nullable=True))
    op.add_column('tests', sa.Column('img_url', mysql.VARCHAR(length=64), nullable=True))
    # ### end Alembic commands ###