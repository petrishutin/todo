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

build_compose:
	docker-compose build

dev_up:
	docker-compose up --build filestorage mongo

test: build_compose
	docker-compose run -e MONGO_URI=mongodb://mongo:27017 -e FILE_STORAGE_URL=http://filestorage:8000 --rm app /wait-for-it.sh mongo:27017 -- /wait-for-it.sh filestorage:8000 -- pytest -vv -s /tests
	docker-compose down

