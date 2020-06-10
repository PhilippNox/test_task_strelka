# https://www.tutorialspoint.com/lua/lua_relational_operators.htm

from fastapi.logger import logger
import os
from app.schemas import Rqst

path_lua = f'{os.path.dirname(os.path.realpath(__file__))}/redis_lua/'


class RdsOpr:

	def __init__(self):
		self.rds = None
		self.sha_set_state = None

	def set_up_rds(self, rds):
		self.rds = rds

	async def full_set_up(self, rds, log=True):
		self.set_up_rds(rds)
		rlt_flush = await self.rds.script_flush()
		if log:
			logger.info(f"RdsOpr 💾 : script_flush {rlt_flush}")
		await self.set_up_scripts([
			'set_state',
		], log=log)

	async def set_up_scripts(self, scripts, log=False):
		for item in scripts:
			with open(f'{path_lua}{item}.lua', 'r') as txt:
				script = ''.join(txt.readlines())
			rlt = await self.rds.script_load(script)
			self.__setattr__(f"sha_{item}", await self.rds.script_load(script))
			if log:
				logger.info(f"RdsOpr 💾 : setup script for REDIS: sha_{item} {rlt}")

	def raw(self):
		return self.rds

	async def set_state(self, chat_id, state):
		return await self.rds.evalsha(
			self.sha_set_state,
			keys=[chat_id, state]
		)

rdsopr = RdsOpr()

