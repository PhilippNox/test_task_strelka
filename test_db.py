from app.db.core_db import database
from app.db.models import user, goods
from app.db.crud import *
import sqlalchemy as sa
from sqlalchemy.sql.expression import join
import app.schemas as schemas
from app.core.exception_bot import BotExceptionNoUser
import asyncio
from fastapi.logger import logger
from asyncpg.exceptions import UniqueViolationError
from typing import Optional
import app.schemas_db as sch_db
import app.db.crud_goods as crud_goods
import app.db.crud_account as crud_account
import uuid
import random


async def test_crud_goods():
	rlt = await crud_goods.create_goods(name='grenny smith', quantity=4, price=39.9, barcode=42)
	print(rlt)
	rlt = await crud_goods.create_goods(name='grenny smith', quantity=4, price=39.9, barcode=420)
	print(rlt)
	rlt = await crud_goods.get_list_of_goods()
	print(rlt)


async def test_crud_account():
	rlt = await crud_account.create_account(current_balance=round(random.uniform(10.0, 1000.0), 2))
	print(rlt)
	# ForeignKeyViolationError
	# print(await crud_account.create_account(current_balance=979.78, deal_uuid=uuid.uuid4()))
	print(await crud_account.get_balance())



async def run_test():
	await database.connect()

	#await test_crud_goods()
	await test_crud_account()

	await database.disconnect()


async def main():
	await asyncio.gather(run_test())


asyncio.run(main())

# export DYLD_FALLBACK_LIBRARY_PATH=$HOME/anaconda/lib/:$DYLD_FALLBACK_LIBRARY_PATH
# python test_db_goods.py
