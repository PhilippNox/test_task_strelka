import app.schemas as schemas
from app.driver.tg import tg_driver
from app.msg_text import msg_zero as msg
from app.core.redisbot import rdsopr
from app.bot_logic.state_holder import state_holder
import app.api_logic as api
from app.db import crud_goods
from . import case_zero


async def handle_init(rqst: schemas.Rqst):
	await rdsopr.set_state(rqst.chat_id, state_holder.buy)
	await tg_driver.send_msg(rqst.chat_id, 'state -> buy')


async def handle(rqst: schemas.Rqst):
	await tg_driver.send_msg(rqst.chat_id, 'state -> zero')
	await case_zero.handle_init(rqst)
