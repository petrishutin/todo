# TODO_MONGO

## Description

Simple TODO backend app with JWT authorization using MongoDB and FastAPI.

## Stack

- Python 3.11
- FastAPI(api) + beanie(ODM) + fastapi_jwt_auth(authorization)
- MongoDB(DB)

## Run

### run stack locally in docker-compose

``` shellsession
make up 
```

### run tests in docker-compose

``` shellsession
make tests
```

### run MongoDB for local development

``` shellsession
make run_mongo
```