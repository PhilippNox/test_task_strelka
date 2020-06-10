# Core
export DYLD_FALLBACK_LIBRARY_PATH=$HOME/anaconda/lib/:$DYLD_FALLBACK_LIBRARY_PATH
uvicorn app.main:app --reload
curl -i -X POST -d '{"msg":"hello"}' http://localhost:8000/echo -w '\n'


# SQL / MIGRATIONS
alembic revision -m "create account table"
    # https://stackoverflow.com/a/30726895/9016251
export DYLD_FALLBACK_LIBRARY_PATH=$HOME/anaconda/lib/:$DYLD_FALLBACK_LIBRARY_PATH
alembic upgrade head


# MAIN
./run_local_bot.sh


# For test sql requests
./test_db.py
