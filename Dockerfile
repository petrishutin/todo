FROM python:3.11.2 as prod
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN python -m pip install --upgrade pip
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY ./scripts/entrypoint.sh /
COPY ./scripts/wait-for-it.sh /
COPY ./.env /app
COPY ./app /app

FROM prod as dev
COPY ./requirements-dev.txt /app
RUN pip install -r requirements-dev.txt
COPY ./tests /tests
ENV PYTHONPATH=/
