deps:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

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

up:
	docker-compose -f docker-compose-test.yaml up --build

down:
	docker-compose -f docker-compose-test.yaml down

rebuild:
	docker-compose -f docker-compose-test.yaml up -d --build app

test: down
	docker-compose -f docker-compose-test.yaml build
	docker-compose -f docker-compose-test.yaml run --rm app /wait-for-it.sh mongo:27017 localstack:4563 -- pytest -s ../tests
	docker-compose -f docker-compose-test.yaml down
