from typing import Optional, Any, List
from pydantic import BaseModel


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

