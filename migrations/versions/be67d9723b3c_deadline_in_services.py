"""deadline in services

Revision ID: be67d9723b3c
Revises: 1a1b24ae1608
Create Date: 2023-01-17 12:37:09.495749

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be67d9723b3c'
down_revision = '1a1b24ae1608'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('services', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deadline', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('services', schema=None) as batch_op:
        batch_op.drop_column('deadline')

    # ### end Alembic commands ###
