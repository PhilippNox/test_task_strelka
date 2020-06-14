from pydantic import BaseModel


class Goods(BaseModel):
	name: str
	quantity: int
	price: float
	barcode: int
