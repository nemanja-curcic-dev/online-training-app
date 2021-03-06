"""empty message

Revision ID: f4133827ef9d
Revises: f2b47e8f1253
Create Date: 2018-12-19 22:35:01.655618

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f4133827ef9d'
down_revision = 'f2b47e8f1253'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('anthropometry_users_tests')
    op.add_column('anthropometry_tests', sa.Column('body_fat_mass', sa.Integer(), nullable=True))
    op.add_column('anthropometry_tests', sa.Column('body_fat_percentage', sa.Integer(), nullable=True))
    op.add_column('anthropometry_tests', sa.Column('date_done', sa.DateTime(), nullable=True))
    op.add_column('anthropometry_tests', sa.Column('muscle_mass', sa.Integer(), nullable=True))
    op.add_column('anthropometry_tests', sa.Column('muscle_mass_percentage', sa.Integer(), nullable=True))
    op.add_column('anthropometry_tests', sa.Column('thigh', sa.Integer(), nullable=True))
    op.add_column('anthropometry_tests', sa.Column('waist', sa.Integer(), nullable=True))
    op.add_column('anthropometry_tests', sa.Column('weight', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('anthropometry_tests', 'weight')
    op.drop_column('anthropometry_tests', 'waist')
    op.drop_column('anthropometry_tests', 'thigh')
    op.drop_column('anthropometry_tests', 'muscle_mass_percentage')
    op.drop_column('anthropometry_tests', 'muscle_mass')
    op.drop_column('anthropometry_tests', 'date_done')
    op.drop_column('anthropometry_tests', 'body_fat_percentage')
    op.drop_column('anthropometry_tests', 'body_fat_mass')
    op.create_table('anthropometry_users_tests',
    sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('test_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('date_done', mysql.DATETIME(), nullable=True),
    sa.Column('weight', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('waist', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('thigh', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('body_fat_percentage', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('body_fat_mass', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('muscle_mass_percentage', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('muscle_mass', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['test_id'], ['anthropometry_tests.id'], name='anthropometry_users_tests_ibfk_1'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='anthropometry_users_tests_ibfk_2'),
    sa.PrimaryKeyConstraint('user_id', 'test_id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
