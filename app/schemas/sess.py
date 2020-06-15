from typing import Optional, List
from pydantic import BaseModel
import app.schemas_db as sch_db


class SessBase(BaseModel):
	state: str
	last_but_msg: Optional[int] = None


class GoodsChoice(sch_db.Goods):
	choice: int = 0


class SessBuy(SessBase):
	cart: List[GoodsChoice]
	cart_idx: int = 0
