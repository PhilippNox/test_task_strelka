from app.db.core_db import database
from app.db.models import account
import app.schemas_db as sch_db
from fastapi.logger import logger
from asyncpg.exceptions import UniqueViolationError
from typing import Optional
import sqlalchemy as sa


async def create_account(current_balance: float, deal_uuid: Optional[str] = None):
	try:
		query = account.insert().values(
			balance=current_balance,
			deal_uuid=deal_uuid
		)
		rlt = await database.execute(query)
		return sch_db.Report(ok=True, code=0, msg="Account update", data=rlt)
	except UniqueViolationError as e:
		return sch_db.Report(ok=False, code=2, msg="One deal can have only one row", data=e.detail)
	except Exception as e:  # TODO ForeignKeyViolationError
		logger.warning(f"create_account: Exception: {e}")
		return sch_db.Report(ok=False, code=1, msg="Unknown error", data=e)


async def get_balance():
	try:
		query = sa.select([account.c.balance]).order_by(account.c.id.desc()).limit(1)
		rlt = await database.fetch_one(query)
		return sch_db.ReportBalance(ok=True, code=0, msg="Current balance", data=rlt['balance'])
	except Exception as e:
		logger.warning(f"get_balance: Exception: {e}")
		return sch_db.ReportBalance(ok=False, code=1, msg="Unknown error", data=e)
