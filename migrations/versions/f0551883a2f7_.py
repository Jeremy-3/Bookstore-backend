"""empty message

Revision ID: f0551883a2f7
Revises: 624989de0730
Create Date: 2025-01-30 12:29:26.190046

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0551883a2f7'
down_revision = '624989de0730'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bookstore_books', 'created_at')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookstore_books', sa.Column('created_at', sa.DATETIME(), nullable=True))
    # ### end Alembic commands ###
