from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
	TG_WEBHOOK_MAIN:	str
	TG_TOKEN_MAIN:		str
	DB_HOST:			str
	DB_PORT:			str
	DB_USER:			str
	DB_PASSWORD: 		str
	DB_DATABASE:		str
	BOT_NAME:			str
	DEF_USER:			str

	class Config:
		env_file = '.env'


settings = Settings()
