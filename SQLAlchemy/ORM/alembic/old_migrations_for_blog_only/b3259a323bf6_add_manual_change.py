"""Add manual change

Revision ID: b3259a323bf6
Revises: 49367a22b507
Create Date: 2021-06-12 13:20:39.350898

"""
from alembic import op
import sqlalchemy as sa
import imp
import os
alembic_helpers = imp.load_source('alembic_helpers', (
    os.getcwd() + '/' + op.get_context().script.dir + '/alembic_helpers.py'))


# revision identifiers, used by Alembic.
revision = 'b3259a323bf6'
down_revision = '49367a22b507'
branch_labels = None
depends_on = None


def upgrade():
    print(alembic_helpers.table_exists("Book"))


def downgrade():
    pass
