from typing import Optional
from app.core.config import settings
import aiohttp
from app.core.redisbot import rdsopr
import app.schemas as schemas
bas_url = 'https://api.telegram.org/bot'


class TgDriver:

	prefix_memory_vault = set()

	def __init__(self, token: str, prefix_memory: str = None):
		if prefix_memory in self.prefix_memory_vault:
			raise Exception()
		self.prefix_memory_vault.add(prefix_memory)
		self.msg_url = f'{bas_url}{token}/sendMessage'
		self.but_url = f'{bas_url}{token}/editMessageReplyMarkup'
		self.del_url = f'{bas_url}{token}/deleteMessage'
		self.edt_url = f'{bas_url}{token}/editMessageText'
		self.ins_url = f'{bas_url}{token}/answerCallbackQuery'
		self.pho_url = f'{bas_url}{token}/sendPhoto'
		self.pre_mem = prefix_memory

	def mem(self, chat_id: str):
		if self.pre_mem:
			return f'{self.pre_mem}{chat_id}'
		return chat_id

	async def auto_clear_but(self, incm: schemas.IncmCallback):
		resp = await self.clear_but(incm.chat_id, incm.message_from)
		return resp

	async def send_msg(self, chat_id: str, text: str, buttons=None):
		async with aiohttp.ClientSession() as client:
			if not buttons:
				resp = await client.post(self.msg_url, json={'chat_id': chat_id, 'text': text})
				return resp.status

			resp = await client.post(self.msg_url, json={
				'chat_id': chat_id,
				'text': text,
				'reply_markup': {'inline_keyboard': buttons}
			})
			if resp.status == 200:
				body = await resp.json()
				await rdsopr.raw().hset(
					self.mem(chat_id),
					'last_but_msg',
					body['result']['message_id']
				)
			return resp.status

	async def resend_msg(self, chat_id: str, sess: schemas.SessBase, text: str, buttons=None):
		if sess.last_but_msg:
			await self.delete_msg(chat_id, sess.last_but_msg)
		return await self.send_msg(chat_id, text, buttons)

	async def clear_but(self, chat_id: str, msg_id: int):
		async with aiohttp.ClientSession() as client:
			resp = await client.post(self.but_url, json={
				'chat_id': chat_id,
				'message_id': msg_id
			})
			return resp.status

	async def delete_msg(self, chat_id: str, msg_id: int):
		async with aiohttp.ClientSession() as client:
			resp = await client.post(self.del_url, json={
				'chat_id': chat_id,
				'message_id': msg_id
			})
			if resp.status != 200:  # if not try to clear button
				resp = await client.post(self.but_url, json={
					'chat_id': chat_id,
					'message_id': msg_id
				})
		return resp.status


tg_driver = TgDriver(settings.TG_TOKEN_MAIN)
