"""0_users_bot

Revision ID: 2ea65dddd3aa
Revises: 
Create Date: 2020-06-10 18:38:04.443651

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
revision = '2ea65dddd3aa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created_at', sa.DateTime, server_default=utcnow()),
        sa.Column('updated_at', sa.DateTime, onupdate=utcnow()),
        sa.Column('chat_id', sa.String(20), nullable=False, index=True, unique=True),
    )


def downgrade():
    op.drop_table('users')


