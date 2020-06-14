"""2_deals

Revision ID: 012ed4e15c3b
Revises: cd5d4de8cfd3
Create Date: 2020-06-10 18:49:39.547288

"""
from alembic import op
import sqlalchemy as sa

# 🌟
from sqlalchemy.dialects.postgresql import UUID, ENUM
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
revision = '012ed4e15c3b'
down_revision = 'cd5d4de8cfd3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'deals',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('uuid', UUID),
        sa.Column('created_at', sa.DateTime, server_default=utcnow()),
        sa.Column('user_id', sa.Integer, sa.ForeignKey("users.id")),
        sa.Column('amount', sa.Numeric),
        sa.Column('balance', sa.Numeric),
    )


def downgrade():
    op.drop_table('deals')

