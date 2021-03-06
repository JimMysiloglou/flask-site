"""article_section_ids added

Revision ID: 38987dd3642e
Revises: 1148a22616ee
Create Date: 2022-06-15 23:01:08.436100

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38987dd3642e'
down_revision = '1148a22616ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('article_section_ids', sa.String(length=60), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'article_section_ids')
    # ### end Alembic commands ###
