cd <where is this file located>

alembic downgrade base; alembic upgrade head

uvicorn app.main:app --reload


# Create goods
curl -i -X POST -d '{"name":"granny smith", "quantity": 10, "price": 50, "barcode": 42}' http://localhost:8000/set_goods -w '\n'
curl -i -X POST -d '{"name":"red apple", "quantity": 10, "price": 25, "barcode": 16}' http://localhost:8000/set_goods -w '\n'


# Get_list_of_goods
curl -i -X GET http://localhost:8000/get_list_goods -w '\n'


# Get_level
curl -i -X GET http://localhost:8000/get_level -w '\n'


# Testing /buy
curl -i -X POST -d '{"msg":"hello"}' http://localhost:8000/buy -w '\n'
curl -i -X POST -d '{"id":101, "items": [{"barcode":51, "quantity": 1}]}' http://localhost:8000/buy -w '\n'
curl -i -X POST -d '{"id":101, "items": [{"barcode":42, "quantity": 1000}]}' http://localhost:8000/buy -w '\n'
curl -i -X POST -d '{"id":101, "items": [{"barcode":42, "quantity": 1}]}' http://localhost:8000/buy -w '\n'


# Get_list_of_goods & Get_level
curl -i -X GET http://localhost:8000/get_list_goods -w '\n'
curl -i -X GET http://localhost:8000/get_level -w '\n'


# Testing /sell
curl -i -X POST -d '{"id":101, "items": [{"barcode":51, "quantity": 1}]}' http://localhost:8000/sell -w '\n'
curl -i -X POST -d '{"id":101, "items": [{"barcode":16, "quantity": 100}]}' http://localhost:8000/sell -w '\n'
curl -i -X POST -d '{"id":101, "items": [{"barcode":16, "quantity": 1}]}' http://localhost:8000/sell -w '\n'
curl -i -X POST -d '{"id":101, "items": [{"barcode":16, "quantity": 1}]}' http://localhost:8000/sell -w '\n'
curl -i -X POST -d '{"id":101, "items": [{"barcode":16, "quantity": 1}]}' http://localhost:8000/sell -w '\n'
