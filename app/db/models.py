from app.db.core_db import metadata

from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, DOUBLE_PRECISION, ENUM

user = Table(
	"users",
	metadata,
	Column("id", Integer, primary_key=True, index=True),
	Column("created_at", DateTime),
	Column("updated_at", DateTime),
	Column("chat_id", String, nullable=False, index=True),
)
