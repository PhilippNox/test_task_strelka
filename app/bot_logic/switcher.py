import app.schemas as schemas
from .state_holder import state_holder
from . import case_zero, case_buy
from app.core.exception_bot import BotExceptionNoUser
from app.driver.tg import tg_driver
from app.core.redisbot import rdsopr
from app.msg_text import msg_switcher
from fastapi.logger import logger


async def warning_n_del(chat_id: str):
	logger.warning(f"BotExceptionNoUser for {chat_id} where warning_n_del()")
	await tg_driver.send_msg(chat_id, msg_switcher.no_user)
	await rdsopr.raw().delete(chat_id)


async def switcher_handle(rqst: schemas.Rqst):
	try:
		if rqst.sess.state == state_holder.zero:
			return await case_zero.handle(rqst)
		if rqst.sess.state == state_holder.buy:
			return await case_buy.handle(rqst)
	except BotExceptionNoUser as e:
		logger.warning(f"BotExceptionNoUser for {rqst.chat_id} where {e.where}")
		await tg_driver.send_msg(rqst.chat_id, msg_switcher.no_user)
		await rdsopr.raw().delete(rqst.chat_id)
	except Exception as e:
		logger.warning(f"Exception in switcher for {rqst.chat_id} with {e}")
	return
