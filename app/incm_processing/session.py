import app.schemas as schemas
from fastapi.logger import logger
from app.core.redisbot import rdsopr
from app.bot_logic.state_holder import state_holder
import app.db.crud_user as crud_us


def get_sess(load):
	out = None
	try:
		out = schemas.SessBase(**load)
	finally:
		return out


async def load_session(chat_id) -> schemas.SessBase:
	load = await rdsopr.raw().hgetall(chat_id)
	out = None
	if load:
		out = get_sess(load)
	if out:
		logger.debug(f"load_session= 📲 - from redis")
		return out

	user_db = await crud_us.exist_user(chat_id)
	if not user_db.ok:
		await crud_us.create_user(chat_id)
		logger.debug(f"load_session= 🆕 - create new user")
	else:
		logger.debug(f"load_session= ♻️  - just create new redis session")

	await rdsopr.set_state(chat_id, state_holder.zero)
	return schemas.SessBase(state=state_holder.zero)
