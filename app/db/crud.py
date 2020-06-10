from app.db.core_db import database
from app.db.models import user
import sqlalchemy as sa
from sqlalchemy.sql.expression import join
import app.schemas as schemas
from app.core.exception_bot import BotExceptionNoUser


async def exist_user(chat_id: str) -> schemas.Report:
	query = user.select() \
		.where(user.c.chat_id == chat_id) \
		.order_by(user.c.id.desc())
	out = await database.fetch_one(query=query)
	if not out:
		return schemas.Report(False, 1, "User doesn't exist")
	return schemas.Report(True, 0, "User Exist", out['id'])


async def create_user(chat_id: str):
	query = user.insert().values(chat_id=chat_id)
	return await database.execute(query)
