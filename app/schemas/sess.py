from pydantic import BaseModel


class SessBase(BaseModel):
	state: str
