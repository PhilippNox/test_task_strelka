from typing import Optional, Any
from .incm import Incm
from .sess import SessBase
from pydantic import BaseModel


class Rqst(BaseModel):
	chat_id: str
	incm: Incm
	sess: SessBase
	background_tasks: Any
