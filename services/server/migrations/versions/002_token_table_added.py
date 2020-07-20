"""Token table added

Revision ID: 002
Revises: 001
Create Date: 2020-05-26 06:39:00.766116

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tokens',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('access_token', sa.String(length=200), nullable=False),
    sa.Column('refresh_token', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tokens')
    # ### end Alembic commands ###