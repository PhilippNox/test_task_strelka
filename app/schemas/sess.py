from typing import Optional, List
from pydantic import BaseModel


class SessBase(BaseModel):
	state: str
	last_but_msg: Optional[int] = None
