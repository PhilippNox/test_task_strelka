import app.schemas as schemas
from app.driver.tg import tg_driver
from app.msg_text import msg_zero


async def handle(rqst: schemas.Rqst):
	if type(rqst.incm) is schemas.IncmTxt:
		print(rqst.chat_id, f'{msg_zero.echo}\n{rqst.incm.txt}')
		await tg_driver.send_msg(rqst.chat_id, f'{msg_zero.echo}\n{rqst.incm.txt}')
