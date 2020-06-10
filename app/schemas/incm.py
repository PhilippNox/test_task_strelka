from pydantic import BaseModel
from typing import Optional


class Incm(BaseModel):
	chat_id: str


class IncmTxt(Incm):
	txt: str


class IncmCmd(Incm):
	cmd: str


class IncmDeepLink(IncmCmd):
	deeplink: str


class IncmCallback(Incm):
	callback_query_id: int
	message_from: int
	back: str


class IncmCallbackJson(IncmCallback):
	action: str
	data: Optional[str] = None


class IncmLocation(Incm):
	latitude: float
	longitude: float
