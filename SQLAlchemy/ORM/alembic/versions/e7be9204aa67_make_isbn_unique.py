"""make ISBN unique

Revision ID: e7be9204aa67
Revises: 347126fc065d
Create Date: 2021-06-13 18:13:01.551568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7be9204aa67'
down_revision = '347126fc065d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Book', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_Book_ISBN'), ['ISBN'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Book', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_Book_ISBN'))

    # ### end Alembic commands ###
