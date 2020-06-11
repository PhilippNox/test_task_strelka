from app.db.core_db import metadata

from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID, DOUBLE_PRECISION, ENUM

user = Table(
	"users",
	metadata,
	Column("id", Integer, primary_key=True, index=True),
	Column("created_at", DateTime),
	Column("updated_at", DateTime),
	Column("chat_id", String, nullable=False, index=True),
)

goods = Table(
    'goods',
	metadata,
    Column('id', Integer, primary_key=True),
	Column('created_at', DateTime),
	Column('updated_at', DateTime),
	Column('name', String(255), nullable=False),
    Column('barcode', Integer),  # EAN-8
    Column('quantity', Integer),
    Column('price', Numeric),
)