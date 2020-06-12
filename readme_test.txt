

# Testing /buy
run:
	python test_db.py with await test_crud_goods()
curl -i -X POST -d '{"msg":"hello"}' http://localhost:8000/buy -w '\n'
curl -i -X POST -d '{"id":42, "items": [{"barcode":420, "quantity": 1}]}' http://localhost:8000/buy -w '\n'
curl -i -X POST -d '{"id":42, "items": [{"barcode":420, "quantity": 1000}]}' http://localhost:8000/buy -w '\n'
curl -i -X POST -d '{"id":42, "items": [{"barcode":421, "quantity": 1}]}' http://localhost:8000/buy -w '\n'