from app.db.models import goods, deals, countbook
from app.db.crud import *
import sqlalchemy as sa

import app.schemas_income as sch_in

from fastapi.logger import logger

import app.schemas_db as sch_db
import app.db.crud as crud
import app.db.crud_account as crud_account
import uuid
from typing import List
from decimal import *


async def deal_goods_out(income: sch_in.BuyRequest):
	try:
		rlt = await check_goods_exist(income.items)  # TODO add typing
		if not rlt.ok:
			return rlt
		units, amount = rlt.data[0], rlt.data[1]
		contractor = await crud.get_or_create_user(income.id)
		rlt = await goods_out_trans(contractor, units, amount)
		return rlt
	except Exception as e:
		logger.warning(f"deal_goods_out: Exception: {e}")
		return sch_db.Report(ok=False, code=1, msg="Unknown error")


async def check_goods_exist(to_check: List[sch_in.DealItem]):
	units = dict()
	amount = Decimal(0.0)
	for elem in to_check:
		query = sa.select([goods.c.id, goods.c.price]) \
			.where(goods.c.barcode == elem.barcode)
		rlt = await database.fetch_one(query=query)
		if not rlt:
			return sch_db.Report(ok=False, code=2, msg="Item doesn't exist", data=elem.barcode)
		unit_id, unit_price = rlt['id'], rlt['price']  # TODO check price exist
		units[unit_id] = units.get(unit_id, 0) + elem.quantity
		amount += elem.quantity * unit_price
	return sch_db.Report(ok=True, code=0, msg="List of item for deal", data=(units, amount))


async def goods_out_trans(contractor, units, amount):
	transaction = await database.transaction()
	try:
		rlt = await update_quantity_goods(units)
		if not rlt.ok:
			await transaction.rollback()
			return rlt

		deal_uuid = await create_deal(contractor, amount)
		await update_countbook(units, deal_uuid)
		await update_account(amount, deal_uuid)
		await transaction.commit()
		return sch_db.Report(ok=True, code=0, msg="Deal_out done", data=deal_uuid)
	except Exception as e:
		await transaction.rollback()
		logger.warning(f"goods_out_trans: Exception: {e}")
		return sch_db.Report(ok=False, code=3, msg="Unknown error in trans")


async def update_quantity_goods(units):
	for goods_id, quantity in units.items():
		stmt = goods.update(). \
			where(goods.c.id == goods_id). \
			values(quantity=goods.c.quantity - quantity). \
			returning(goods.c.quantity)
		rlt = await database.execute(stmt)
		if rlt < 0:
			return sch_db.Report(
				ok=False,
				code=4,
				msg=f'not_enough quantity of goods',
				data=(goods_id, -rlt)  # TODO replace goods_id to barcode
			)
	return sch_db.Report(ok=True, code=0, msg=f'quantity updated')


async def create_deal(contractor, amount):
	deal_uuid = uuid.uuid4()
	query = deals.insert().values(
		uuid=deal_uuid,
		contractor=contractor,
		state='goods_out',
		amount=amount,
	)
	await database.execute(query)
	return deal_uuid


async def update_countbook(units, deal_uuid):
	for goods_id, quantity in units.items():
		query = countbook.insert().values(
			goods_id=goods_id,
			quantity=quantity,
			deal_uuid=deal_uuid,
		)
		await database.execute(query)


async def update_account(amount, deal_uuid):
	balance = await crud_account.get_balance()
	if balance.ok:
		await crud_account.create_account(Decimal(balance.data) + amount, deal_uuid)


