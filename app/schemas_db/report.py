from typing import Optional, Any, List
from pydantic import BaseModel
import app.schemas_income as sch_in


class Goods(BaseModel):
	name: str
	quantity: int
	price: float
	barcode: Optional[int] = None


class ReportBase(BaseModel):
	ok:		bool
	code: 	int
	msg:	str


class Report(ReportBase):
	data: Optional[Any] = None


class ReportGoods(ReportBase):
	data: List[Goods]


class ReportLevel(ReportBase):
	data: float


class ReportBalance(ReportBase):
	data: float


class DealItemDB(sch_in.DealItem):
	db_id: int
