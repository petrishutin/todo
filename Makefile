run_mongo:
	docker run -d -p 27017:27017 -e MONGO_INITDB_DATABASE=try_mongo -e MONGO_INITDB_ROOT_USERNAME=test -e MONGO_INITDB_ROOT_PASSWORD=test --name try_mongo mongo

stop_mongo:
	docker stop try_mongo
	docker rm try_mongo

lint:
	black .
	isort .
	flake8 .
	mypy .
