from fastapi.logger import logger
import app.schemas as schemas
from app.driver.tg import tg_driver
from app.msg_text import msg_buy as msg
from app.core.redisbot import rdsopr
from app.bot_logic.state_holder import state_holder
import app.api_logic as api
from app.db import crud_goods
from . import case_zero

from typing import List
from pydantic import BaseModel
import app.schemas_income as sch_in
import app.schemas as sch

import app.db.crud_deal_out as crud_deal_out

import json

but_back = "back"
but_next = "next"
but_quit = "quit"
but_buy = "buy_action"


async def save_sess(chat_id, sess):
	to_save = sess.dict()
	to_save['cart'] = json.dumps(to_save['cart'])
	await rdsopr.raw().hmset_dict(chat_id, to_save)


def buttons(sess):
	base = [[
			{
				'text': '< back',
				'callback_data': but_back,
			},
			{
				'text': 'next >',
				'callback_data': but_next,
			}
		],
		[{
			'text': 'quit',
			'callback_data': but_quit,
		}],
		[{
			'text': 'buy',
			'callback_data': but_buy,
		}],
	]
	if sess.cart_idx == 0:
		base[0].pop(0)
	elif sess.cart_idx == len(sess.cart) - 1:
		base[0].pop()
	return base


async def show_curr_item(rqst: schemas.Rqst):
	item = rqst.sess.cart[rqst.sess.cart_idx]
	msg_show = msg.cart_item.safe_substitute(
		name=item.name,
		barcode=item.barcode,
		quantity=item.quantity,
		price=item.price,
		choice=item.choice
	)
	await tg_driver.resend_msg(rqst.chat_id, rqst.sess, msg_show, buttons(rqst.sess))


async def handle_init(rqst: schemas.Rqst):
	cart = await crud_goods.get_list_of_goods()
	if cart.ok:
		rqst.sess = sch.SessBuy(
			state=state_holder.buy,
			last_but_msg=rqst.sess.last_but_msg,
			cart=[sch.GoodsChoice(**e.dict()) for e in cart.data],
		)
		await save_sess(rqst.chat_id, rqst.sess)
	await show_curr_item(rqst)


async def handle(rqst: schemas.Rqst):
	if type(rqst.incm) is schemas.IncmCallback:
		if rqst.incm.back == but_back:
			rqst.sess = sch.SessBuy(
				**rqst.sess.dict(exclude={'cart_idx'}),
				cart_idx=rqst.sess.cart_idx - 1
			)
			await save_sess(rqst.chat_id, rqst.sess)
			return await show_curr_item(rqst)
		if rqst.incm.back == but_next:
			rqst.sess = sch.SessBuy(
				**rqst.sess.dict(exclude={'cart_idx'}),
				cart_idx=rqst.sess.cart_idx + 1
			)
			await save_sess(rqst.chat_id, rqst.sess)
			return await show_curr_item(rqst)
		if rqst.incm.back == but_quit:
			return await case_zero.handle_init(rqst)
		if rqst.incm.back == but_buy:
			rlt = await crud_deal_out.deal_out(
				sch_in.DealRequest(
					id=rqst.chat_id,
					items=[sch_in.DealItem(barcode=e.barcode, quantity=e.choice)
						   for e in rqst.sess.cart if e.choice != 0]
				)
			)
			if rlt.ok:
				await tg_driver.send_msg(rqst.chat_id, str(rlt.data))
				return await case_zero.handle_init(rqst)

	if type(rqst.incm) is schemas.IncmTxt and rqst.incm.txt.isdigit():
		cart_idx = rqst.sess.cart_idx
		item = rqst.sess.cart[rqst.sess.cart_idx]
		num = int(rqst.incm.txt)
		if num < item.quantity:
			tmp = rqst.sess.dict()
			tmp['cart'][cart_idx]['choice'] = num
			rqst.sess = sch.SessBuy(**tmp)
			await save_sess(rqst.chat_id, rqst.sess)
			return await show_curr_item(rqst)

	await show_curr_item(rqst)
