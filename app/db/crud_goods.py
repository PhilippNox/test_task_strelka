from app.db.core_db import database
from app.db.models import goods
import app.schemas_db as sch_db
from fastapi.logger import logger
from asyncpg.exceptions import UniqueViolationError
from typing import Optional
import sqlalchemy as sa


async def create_goods(name: str, quantity: int, price: float, barcode: Optional[int] = None):
	try:
		query = goods.insert().values(
			name=name,
			barcode=barcode,
			quantity=quantity,
			price=price,
		)
		rlt = await database.execute(query)
		return sch_db.Report(ok=True, code=0, msg="Goods created", data=rlt)
	except UniqueViolationError as e:
		return sch_db.Report(ok=False, code=2, msg="Can't create a duplicate of goods")
	except Exception as e:
		logger.warning(f"create_goods: Exception: {e}")
		return sch_db.Report(ok=False, code=1, msg="Unknown error")


async def get_list_of_goods() -> sch_db.ReportGoods:
	try:
		query = sa.select([
			goods.c.name,
			goods.c.barcode,
			goods.c.quantity,
			goods.c.price,
		])
		rlt = await database.fetch_all(query=query)
		if rlt:
			rlt = [sch_db.Goods(**dict(elem.items())) for elem in rlt]
		return sch_db.ReportGoods(ok=True, code=0, msg="List of goods", data=rlt)
	except Exception as e:
		logger.warning(f"get_list_of_goods: Exception: {e}")
		return sch_db.ReportGoods(ok=False, code=1, msg="Unknown error")
