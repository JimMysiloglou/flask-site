"""language_id added for both articles and projects

Revision ID: 54d71e347c09
Revises: 362c450ff090
Create Date: 2022-06-18 11:15:59.077663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54d71e347c09'
down_revision = '362c450ff090'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('language_id', sa.Integer(), nullable=False))
    op.add_column('project', sa.Column('language_id', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project', 'language_id')
    op.drop_column('article', 'language_id')
    # ### end Alembic commands ###
