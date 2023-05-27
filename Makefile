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

test:
	docker-compose build
	docker-compose run -e MONGO_URI=mongodb://mongo:27017 -e FILE_STORAGE_URL=http://filestorage:8000 --rm app /wait-for-it.sh mongo:27017 -- /wait-for-it.sh filestorage:8000 -- pytest -vv -s /tests
	docker-compose down

build:
	docker build --target prod -t petrishutin/todo_backend:latest .
	docker build --target prod -t us-central1-docker.pkg.dev/flawless-acre-387710/repo1/todo_backend:latest .

push: build
	docker login
	docker push petrishutin/todo_backend:latest
	docker push us-central1-docker.pkg.dev/flawless-acre-387710/repo1/todo_backend:latest
