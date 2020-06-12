from app.db.models import goods, deals, countbook
from app.db.crud import *
import sqlalchemy as sa

import app.schemas_income as sch_in

from fastapi.logger import logger

import app.schemas_db as sch_db
import app.db.crud as crud
import uuid
from decimal import Decimal
from pydantic import BaseModel
from typing import Optional, Any, List
import asyncio
from sqlalchemy import text

errors = {
	'err_except': {'code': 1, 'msg': 'Unknown error'},
	'err_no_goods': {'code': 2, 'msg': "Goods doesn't exist"},
	'err_in_tran': {'code': 3, 'msg': "Unknown error in trans"},
	'err_quantity': {'code': 4, 'msg': "Not enough quantity of a goods"},
}


async def deal_out(income: sch_in.BuyRequest):
	items = income.items
	transaction = await database.transaction()
	try:
		rlts = await list_of_updates(items)
		if None in rlts:
			await transaction.rollback()
			return sch_db.Report(ok=False, code=2, msg=" ", data=get_unknow_barcode(rlts, items))

		quant = [elem['quantity'] for elem in rlts]
		if any(elem < 0 for elem in quant):
			await transaction.rollback()
			return sch_db.Report(ok=False, code=3, msg=" ", data=get_negavite_quant(quant, items))

		deal_uuid = await make_deal_out(income, rlts)
	except Exception as e:
		await transaction.rollback()
		logger.warning(f"deal_out: Exception: {e}")
		return sch_db.Report(ok=False, code=1, msg=" ")
	else:
		await transaction.commit()
	return sch_db.Report(ok=True, code=0, msg=" ", data=deal_uuid)


async def list_of_updates(items: List[sch_in.DealItem]):
	tasks = []
	for elem in items:
		stmt = goods.update(). \
			where(goods.c.barcode == elem.barcode). \
			values(quantity=goods.c.quantity - elem.quantity). \
			returning(goods.c.quantity, goods.c.price, goods.c.id)
		tasks.append(database.fetch_one(stmt))
	return await asyncio.gather(*tasks)


def get_amount(items, rlts):
	out = Decimal(0.0)
	for item, rlt in zip(items, rlts):
		out += item.quantity * rlt['price']
	return out


async def make_deal_out(income, rlts):
	amount = get_amount(income.items, rlts)
	contractor = await crud.get_or_create_user(income.id)
	deal_uuid = uuid.uuid4()
	deal_id = await create_deal(deal_uuid, contractor, amount)
	await update_countbook(income.items, rlts, deal_id)
	return deal_uuid


async def create_deal(deal_uuid, contractor, amount):
	stmt = text(
		f"INSERT INTO deals (uuid, contractor, amount, balance) VALUES ("
		f"'{deal_uuid}', "
		f"'{contractor}', "
		f"'{amount}', "
		f"(SELECT deals.balance FROM deals ORDER BY deals.id DESC LIMIT 1) + {amount})"
		f"RETURNING deals.id")
	return await database.execute(stmt)


async def update_countbook(items, rlts, deal_id):
	tasks = []
	for item, elem in zip(items, rlts):
		query = countbook.insert().values(
			goods_id=elem['id'],
			quantity=item.quantity,
			deal_id=deal_id,
		)
		tasks.append(database.execute(query))
	return await asyncio.gather(*tasks)


def get_unknow_barcode(rlts, items):
	return [x[1].barcode for x in zip(rlts, items) if x[0] is None]


def get_negavite_quant(quant, items):
	return [(x[1].barcode, x[0]) for x in zip(quant, items) if x[0] < 0]
