"""Init

Revision ID: 31ae435340ec
Revises: 
Create Date: 2023-05-27 21:49:47.069190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31ae435340ec'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'role')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('role', sa.VARCHAR(length=9), nullable=True))
    # ### end Alembic commands ###
