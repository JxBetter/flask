"""initial migration

Revision ID: bc3561c74975
Revises: 496e65afb59e
Create Date: 2018-02-14 13:47:08.524552

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc3561c74975'
down_revision = '496e65afb59e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('articles', sa.Column('editstamp', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('articles', 'editstamp')
    # ### end Alembic commands ###
