FROM python:3.11.2-slim as prod
ENV PYTHONUNBUFFERED 1
WORKDIR /
RUN python -m pip install --upgrade pip
COPY ./requirements.txt /
RUN pip install -r requirements.txt
COPY ./scripts/entrypoint.sh /
COPY ./scripts/wait-for-it.sh /
COPY ./app /app

FROM prod as dev
COPY ./requirements-dev.txt /
RUN pip install -r requirements-dev.txt
COPY ./tests /tests
ENV PYTHONPATH=/