"""initial migration

Revision ID: c317542ac48d
Revises: 
Create Date: 2018-02-14 21:23:14.185414

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c317542ac48d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('version_num', sa.String(length=32), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'version_num')
    # ### end Alembic commands ###