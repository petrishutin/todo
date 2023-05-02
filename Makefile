deps:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

lint:
	black .
	isort .
	flake8 .
	mypy .

check:
	black --check .
	isort --check-only .
	flake8 .
	mypy .

up:
	docker-compose up --build

down:
	docker-compose down

dev_up:
	docker-compose up --build filestorage mongo

rebuild:
	docker-compose up -d --build app

test:
	docker-compose up -d filestorage mongo
	sleep 5
	pytest -vv -s
	docker-compose down