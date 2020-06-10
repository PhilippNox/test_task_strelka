from app.db.core_db import database
from app.db.models import user
from app.db.crud import *
import sqlalchemy as sa
from sqlalchemy.sql.expression import join
import app.schemas as schemas
from app.core.exception_bot import BotExceptionNoUser
import asyncio
from fastapi.logger import logger


async def count_users():
	try:
		query = user.count()
		out = await database.execute(query)
	except Exception as e:
		logger.warning(f"count_users: Exception: {e}")
		return schemas.Report(False, 1, "Unknown error", e)
	return schemas.Report(True, 0, "ok", out)



async def run_test():
	await database.connect()

	rlt = await count_users()
	print(rlt)

	await database.disconnect()


async def main():
	await asyncio.gather(run_test())


asyncio.run(main())

# export DYLD_FALLBACK_LIBRARY_PATH=$HOME/anaconda/lib/:$DYLD_FALLBACK_LIBRARY_PATH
# python test_db.py
