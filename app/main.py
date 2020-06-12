from app.core.config import settings
from fastapi.logger import logger
import logging
import aioredis
from fastapi import FastAPI, Request, BackgroundTasks
from app.core.redisbot import rdsopr
import app.schemas as schemas
import app.schemas_db as sch_db
import app.schemas_income as sch_in
from app.db import crud_goods, crud_account

import app.incm_processing as incm_proc

from app.db.core_db import database

from app.bot_logic.switcher import switcher_handle

app = FastAPI()


@app.get("/get_list_goods")
async def get_list_goods():  # response_model=sch_db.ReportGoods
	return await crud_goods.get_list_of_goods()


@app.get("/get_level")
async def get_level():  # response_model=sch_db.ReportLevel
	if settings.HUMAN_NUM < 1:
		return sch_db.ReportLevel(ok=False, code=1, msg="Number of humans less than 1")
	balance = await crud_account.get_balance()
	if not balance.ok:
		return sch_db.ReportLevel(ok=False, code=2, msg="Balance are not available")
	out_data = round(balance.data / settings.HUMAN_NUM * abs(settings.FLOORS_NUM) * 0.01, 3)
	return sch_db.ReportLevel(ok=True, code=0, msg="Current level", data=out_data)


# curl -i -X POST -d '{"msg":"hello"}' http://localhost:8000/buy -w '\n'
# curl -i -X POST -d '{"id":42, "items": [{"barcode":420, "quantity": 1}]}' http://localhost:8000/buy -w '\n'
@app.post("/buy")
async def buy(buy_post: sch_in.BuyRequest):
    return buy_post



@app.post(settings.TG_WEBHOOK_MAIN)
async def telegram_income(request: Request, background_tasks: BackgroundTasks):
	incm = await incm_proc.parser_incm(request)
	if not incm:
		return	 # TODO_maybe notify that useless msg, but how ? Need to parse chat_id
	session = await incm_proc.load_session(incm.chat_id)
	rqst = schemas.Rqst(
		chat_id=incm.chat_id,
		incm=incm,
		sess=session,
		background_tasks=background_tasks,
	)
	await switcher_handle(rqst)


@app.on_event("startup")
async def startup_event():
	logger.setLevel(logging.DEBUG)
	rds = await aioredis.create_redis_pool('redis://localhost', encoding='utf-8')
	await rdsopr.full_set_up(rds)
	await database.connect()


@app.on_event("shutdown")
async def shutdown_event():
	rdsopr.raw().close()
	await rdsopr.raw().wait_closed()
	await database.disconnect()
