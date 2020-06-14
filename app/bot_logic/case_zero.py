import app.schemas as schemas
from app.driver.tg import tg_driver
from app.msg_text import msg_zero as msg
import app.api_logic as api
from app.db import crud_goods
from . import case_buy
from app.core.redisbot import rdsopr
from app.bot_logic.state_holder import state_holder

but_level = "level"
but_goods = "goods"
but_buy = "buy"


def menu_but():
	return [
		[{
			'text': msg.but_text_level,
			'callback_data': but_level,
		}],
		[{
			'text': msg.but_text_goods,
			'callback_data': but_goods,
		}],
		[{
			'text': msg.but_text_buy,
		  	'callback_data': but_buy,
		}],
	]


async def show_level(rqst: schemas.Rqst):
	msg_level = msg.no_level
	rlt = await api.get_level()
	if rlt.ok:
		msg_level = msg.curr_level.safe_substitute(level=rlt.data)
	await tg_driver.resend_msg(rqst.chat_id, rqst.sess, msg_level)
	await tg_driver.send_msg(rqst.chat_id, msg.menu, menu_but())


async def show_goods(rqst: schemas.Rqst):
	msg_goods = msg.no_goods
	rlt = await crud_goods.get_list_of_goods()
	if rlt.ok:
		items_str = [msg.first_line_goods]
		for elem in rlt.data:
			items_str.append(msg.elem_goods.safe_substitute(
				name=elem.name,
				barcode=elem.barcode,
				quantity=elem.quantity,
				price=elem.price,
			))
		msg_goods = "\n".join(items_str)
	await tg_driver.resend_msg(rqst.chat_id, rqst.sess, msg_goods)
	await tg_driver.send_msg(rqst.chat_id, msg.menu, menu_but())


async def handle_init(rqst: schemas.Rqst):
	await rdsopr.set_state(rqst.chat_id, state_holder.zero)
	await tg_driver.send_msg(rqst.chat_id, msg.menu, menu_but())


async def handle(rqst: schemas.Rqst):
	if type(rqst.incm) is schemas.IncmTxt:
		await tg_driver.resend_msg(rqst.chat_id, rqst.sess, msg.menu, menu_but())

	if type(rqst.incm) is schemas.IncmCallback:
		if rqst.incm.back == but_level:
			return await show_level(rqst)
		if rqst.incm.back == but_goods:
			return await show_goods(rqst)
		if rqst.incm.back == but_buy:
			return await case_buy.handle_init(rqst)
