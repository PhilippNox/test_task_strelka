from app.db.core_db import database
from app.db.models import deals
import app.schemas_db as sch_db
from fastapi.logger import logger
from asyncpg.exceptions import UniqueViolationError
from typing import Optional
import sqlalchemy as sa
from decimal import Decimal
import uuid


async def initial_deal():
	try:
		query = sa.select([deals]).order_by(deals.c.created_at.desc()).limit(1)
		rlt = await database.execute(query)
		if not rlt:
			query = deals.insert().values(
				uuid=uuid.uuid4(),
				balance=0.0
			).returning(deals.c.uuid)
			rlt = await database.execute(query)
			logger.info(f"Initial deal created {rlt}")
	except Exception as e:
		logger.warning(f"initial_deal: Exception: {e}")


async def get_balance():
	try:
		query = sa.select([deals.c.balance]).order_by(deals.c.id.desc()).limit(1)
		rlt = await database.execute(query)
		return sch_db.ReportBalance(ok=True, code=0, msg="Current balance", data=rlt)
	except Exception as e:
		logger.warning(f"get_balance: Exception: {e}")
		return sch_db.ReportBalance(ok=False, code=1, msg="Unknown error")
