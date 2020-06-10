# 0. Postgresql: Create a user and database

0.0. Create user and database
	cp .env_example .env
	./init_script.sh

0.1. Make migration:
	alembic upgrade head