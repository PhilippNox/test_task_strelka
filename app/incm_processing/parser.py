import app.schemas as schemas
from fastapi.logger import logger
from fastapi import Request
import json


async def get_incm_txt(body_json):
	out = None
	try:
		out = schemas.IncmTxt(
			chat_id=body_json['message']['chat']['id'],
			txt=body_json['message']['text']
		)
	finally:
		return out


async def get_incm_cmd(body_json) -> schemas.IncmCmd:
	out = None
	try:
		if body_json['message']['entities'][0]['type'] == "bot_command":
			chat_id = body_json['message']['chat']['id']
			cmd = body_json['message']['text']

			if body_json['message']['text'].lower().startswith("/start "):
				out = schemas.IncmDeepLink(chat_id=chat_id, cmd=cmd, deeplink=cmd[7:],)
			else:
				out = schemas.IncmCmd(chat_id=chat_id, cmd=cmd,)
	finally:
		return out


async def get_callback(body_json) -> schemas.IncmCallback:
	out = None
	try:
		out = schemas.IncmCallback(
			chat_id=body_json['callback_query']['message']['chat']['id'],
			callback_query_id=body_json['callback_query']['id'],
			message_from=body_json['callback_query']['message']['message_id'],
			back=body_json['callback_query']['data'],
		)
	finally:
		return out


async def get_callback_json(body_json) -> schemas.IncmCallbackJson:
	out = None
	try:
		back = body_json['callback_query']['data']
		out = schemas.IncmCallbackJson(
			**json.loads(back),
			chat_id=body_json['callback_query']['message']['chat']['id'],
			callback_query_id=body_json['callback_query']['id'],
			message_from=body_json['callback_query']['message']['message_id'],
			back=body_json['callback_query']['data'],
		)
	finally:
		return out


async def get_incm_location(body_json):
	out = None
	try:
		out = schemas.IncmLocation(
			chat_id=body_json['message']['chat']['id'],
			latitude=body_json['message']['location']['latitude'],
			longitude=body_json['message']['location']['longitude'],
		)
	finally:
		return out


async def parser_incm(request: Request) -> schemas.Incm:
	body = await request.json()
	out = await get_incm_cmd(body)
	if not out:
		out = await get_incm_txt(body)
	if not out:
		out = await get_callback_json(body)
	if not out:
		out = await get_callback(body)
	if not out:
		out = await get_incm_location(body)
	if not out:
		logger.warning(f"unknown income: {json.dumps(body)}")
	logger.debug(type(out))
	return out
