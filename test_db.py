from app.db.core_db import database
from app.db.models import user, goods, deals, countbook
from app.db.crud import *
import sqlalchemy as sa
from sqlalchemy.sql.expression import join
import app.schemas as schemas
import app.schemas_income as sch_in
from app.core.exception_bot import BotExceptionNoUser
import asyncio
from fastapi.logger import logger
from asyncpg.exceptions import UniqueViolationError
from typing import Optional
import app.schemas_db as sch_db
import app.db.crud_goods as crud_goods
import app.db.crud_deal_out as crud_deal_out
import uuid
import random
from typing import List
from decimal import *


async def test_crud_goods():
	rlt = await crud_goods.create_goods(name='granny smith', quantity=8000, price=50, barcode=42)
	print(rlt)
	rlt = await crud_goods.create_goods(name='red apple', quantity=8000, price=25, barcode=420)
	print(rlt)
	rlt = await crud_goods.get_list_of_goods()
	print(rlt)


async def test_crud_deal_out():
	# await test_crud_goods()

	test = sch_in.BuyRequest(
		id=101,
		items=[
			sch_in.DealItem(
				barcode=420,
				quantity=1,
			),
			sch_in.DealItem(
				barcode=42,
				quantity=1,
			),
			sch_in.DealItem(
				barcode=420,
				quantity=1,
			),
		]
	)
	print(await crud_deal_out.deal_out(test))


async def run_test():
	await database.connect()

	await test_crud_goods()
	# await test_crud_deal_out()
	# await test_crud_deal_out()
	tasks = []
	for _ in range(0):
		tasks.append(test_crud_deal_out())
	await asyncio.gather(*tasks)

	await database.disconnect()


async def main():
	await asyncio.gather(run_test())


asyncio.run(main())

# export DYLD_FALLBACK_LIBRARY_PATH=$HOME/anaconda/lib/:$DYLD_FALLBACK_LIBRARY_PATH
# python test_db_goods.py
