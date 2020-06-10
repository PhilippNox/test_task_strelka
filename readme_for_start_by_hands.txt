# Postgresql: Create a user and database

0. For check (in other terminal):
	sudo -u postgres psql
    	- then password for sudo
    	- then password for postgres (user postgres)
    \du - show users
    \l 	- show databases

1. Create user:
	sudo -u postgres createuser --interactive -P
		- then password for sudo
		- Enter name of role to add:								vaultboy
		- Enter password for new role:								****
		- Enter it again:											****
		- Shall the new role be a superuser?						n
		- Shall the new role be allowed to create databases? 		y
		- Shall the new role be allowed to create more new roles?	n
		- then password for postgres (user postgres)

2. Create database:
	sudo -u postgres createdb vaultboy -U vaultboy
		- then password for vaultboy

3. Copy data to .env:
	cp .env_example .env
	- add to .env: DB_USER=vaultboy
	- add to .env: DB_PASSWORD=pass_for_vaultboy
	- add to .env: DB_DATABASE=vaultboy

4. Make migration:
	alembic upgrade head