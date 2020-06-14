from app.db.core_db import metadata

from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID, DOUBLE_PRECISION, ENUM

user = Table(
	"users",
	metadata,
	Column("id", Integer, primary_key=True, index=True),
	Column("created_at", DateTime),
	Column("updated_at", DateTime),
	Column("chat_id", String, nullable=False, index=True, unique=True),
)

goods = Table(
	'goods',
	metadata,
	Column('id', Integer, primary_key=True),
	Column('created_at', DateTime),
	Column('updated_at', DateTime),
	Column('name', String(255), nullable=False),
	Column('barcode', Integer, unique=True, index=True),  # EAN-8
	Column('quantity', Integer),
	Column('price', Numeric),
)

deals = Table(
	'deals',
	metadata,
	Column('id', Integer, primary_key=True),
	Column('uuid', UUID),
	Column('created_at', DateTime),
	Column('user_id', Integer, ForeignKey("users.id")),
	Column('amount', Numeric),
	Column('balance', Numeric),
)

countbook = Table(
	'countbook',
	metadata,
	Column('id', Integer, primary_key=True),
	Column('created_at', DateTime),
	Column('goods_id', Integer, ForeignKey("goods.id")),
	Column('quantity', Integer),
	Column('deal_id', Integer, ForeignKey("deals.id")),
)