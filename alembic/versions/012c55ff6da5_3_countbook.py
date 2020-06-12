"""3_countbook

Revision ID: 012c55ff6da5
Revises: 012ed4e15c3b
Create Date: 2020-06-10 19:33:16.315633

"""
from alembic import op
import sqlalchemy as sa

# 🌟
from sqlalchemy.dialects.postgresql import UUID
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
revision = '012c55ff6da5'
down_revision = '012ed4e15c3b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'countbook',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created_at', sa.DateTime, server_default=utcnow()),
        sa.Column('goods_id', sa.Integer, sa.ForeignKey("goods.id")),
        sa.Column('quantity', sa.Integer),
        sa.Column('deal_id', sa.Integer, sa.ForeignKey("deals.id")),
    )


def downgrade():
    op.drop_table('countbook')
