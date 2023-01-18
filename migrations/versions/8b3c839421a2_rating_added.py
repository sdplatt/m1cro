"""rating added

Revision ID: 8b3c839421a2
Revises: be67d9723b3c
Create Date: 2023-01-18 10:11:36.187617

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b3c839421a2'
down_revision = 'be67d9723b3c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('translations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rating', sa.Float(), nullable=True))

    with op.batch_alter_table('translators', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rating', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('rating_count', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('translators', schema=None) as batch_op:
        batch_op.drop_column('rating_count')
        batch_op.drop_column('rating')

    with op.batch_alter_table('translations', schema=None) as batch_op:
        batch_op.drop_column('rating')

    # ### end Alembic commands ###
