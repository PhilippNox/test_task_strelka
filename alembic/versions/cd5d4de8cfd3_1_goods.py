"""1_goods

Revision ID: cd5d4de8cfd3
Revises: 2ea65dddd3aa
Create Date: 2020-06-10 18:39:48.201037

"""
from alembic import op
import sqlalchemy as sa

# 🌟
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime


class utcnow(expression.FunctionElement):
    type = DateTime()


@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"
# end 🌟

# revision identifiers, used by Alembic.
revision = 'cd5d4de8cfd3'
down_revision = '2ea65dddd3aa'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'goods',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created_at', sa.DateTime, server_default=utcnow()),
        sa.Column('updated_at', sa.DateTime, onupdate=utcnow()),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('barcode', sa.Integer, unique=True, index=True),  # EAN-8
        sa.Column('quantity', sa.Integer),
        sa.Column('price', sa.Numeric),
    )


def downgrade():
    op.drop_table('goods')

