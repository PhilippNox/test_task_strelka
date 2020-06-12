from typing import Optional, Any, List
from pydantic import BaseModel


class DealItem(BaseModel):
	barcode: 	int
	quantity: 	int


class BuyRequest(BaseModel):
	id:	str
	items: List[DealItem]
