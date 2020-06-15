# 0. Postgresql: Create a user and database

0.0. Create user and database
	cp .env_example .env
	./init_script.sh

0.1. Make migration:
	alembic upgrade head


# 1. In .env define variables.

1.0. Commune variables
	HUMAN_NUM - positive number
	FLOORS_NUM - positive number

1.1. Bot variables - https://core.telegram.org/bots#3-how-do-i-create-a-bot
	BOT_NAME - name of telegram bot
	TG_TOKEN_MAIN - token for telegram bot
	TG_WEBHOOK_MAIN - end of url like "/tg"

1.2 Test variables - https://ngrok.com/
	NGROK_PATH - abs path to ngrok like "/Users/username/Desktop/ngrok"
	DEF_USER - default user id for telegram


# 2. Run test:

2.0. Just run ./run_local_bot.sh