"""empty message

Revision ID: 3b8a2b517dac
Revises: 4aee72a4c888
Create Date: 2022-05-17 12:05:22.433190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b8a2b517dac'
down_revision = '4aee72a4c888'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('path_original', sa.String(length=100), nullable=False))
        batch_op.create_unique_constraint(None, ['path_original'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('path_original')

    # ### end Alembic commands ###
