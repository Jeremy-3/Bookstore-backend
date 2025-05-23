"""adding is_banned column

Revision ID: fd70030a6e3d
Revises: da086b9aa1b6
Create Date: 2025-05-13 15:18:48.403616

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd70030a6e3d'
down_revision = 'da086b9aa1b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_banned', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_banned')
    # ### end Alembic commands ###
