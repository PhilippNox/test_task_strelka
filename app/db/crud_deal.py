from app.db.core_db import database
from app.db.models import deals, goods, countbook
import app.schemas_db as sch_db
from fastapi.logger import logger
import sqlalchemy as sa
from decimal import Decimal
import uuid
import app.schemas_income as sch_in
from typing import List
import asyncio
from sqlalchemy import text


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


async def create_deal(deal_uuid, contractor, amount):
	stmt = text(
		f"INSERT INTO deals (uuid, contractor, amount, balance) VALUES ("
		f"'{deal_uuid}', "
		f"'{contractor}', "
		f"'{amount}', "
		f"(SELECT deals.balance FROM deals ORDER BY deals.id DESC LIMIT 1) + {amount})"
		f"RETURNING deals.id, deals.balance")
	rlt = await database.fetch_one(stmt)
	return rlt['id'], rlt['balance']


async def update_goods(items: List[sch_in.DealItem], deal_is_out: bool = True):
	tasks = []
	for elem in items:
		if deal_is_out:
			elem_quantity = -elem.quantity
		else:
			elem_quantity = elem.quantity
		stmt = goods.update(). \
			where(goods.c.barcode == elem.barcode). \
			values(quantity=goods.c.quantity + elem_quantity). \
			returning(goods.c.quantity, goods.c.price, goods.c.id)
		tasks.append(database.fetch_one(stmt))
	return await asyncio.gather(*tasks)


async def update_countbook(items, rlts, deal_id, deal_is_out: bool = True):
	tasks = []
	for item, elem in zip(items, rlts):
		if deal_is_out:
			elem_quantity = -item.quantity
		else:
			elem_quantity = item.quantity
		query = countbook.insert().values(
			goods_id=elem['id'],
			quantity=elem_quantity,
			deal_id=deal_id,
		)
		tasks.append(database.execute(query))
	return await asyncio.gather(*tasks)


def get_amount(items, rlts):
	out = Decimal(0.0)
	for item, rlt in zip(items, rlts):
		out += item.quantity * rlt['price']
	return out


def get_unknow_barcode(items, rlts):
	return [x[1].barcode for x in zip(rlts, items) if x[0] is None]


def get_negavite_quant(items, quant):
	return [(x[1].barcode, x[0]) for x in zip(quant, items) if x[0] < 0]
