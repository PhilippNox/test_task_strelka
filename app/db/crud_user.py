from app.db.core_db import database
from app.db.models import user
import sqlalchemy as sa
import app.schemas_db as sch_db


async def exist_user(chat_id: str) -> sch_db.Report:
	query = user.select() \
		.where(user.c.chat_id == chat_id) \
		.order_by(user.c.id.desc())
	out = await database.fetch_one(query=query)
	if not out:
		return sch_db.Report(False, 1, "User doesn't exist")
	return sch_db.Report(True, 0, "User Exist", out['id'])


async def create_user(chat_id: str):
	query = user.insert().values(chat_id=chat_id)
	return await database.execute(query)


async def get_or_create_user(chat_id: str):
	query = sa.select([user.c.id]) \
		.where(user.c.chat_id == chat_id)
	out_id = await database.execute(query=query)
	if not out_id:
		query = user.insert().values(chat_id=chat_id)
		out_id = await database.execute(query)
	return out_id