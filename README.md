# TODO

## Description

Simple TODO backend app with JWT authorization using MongoDB and FastAPI.

## Stack

- Python 3.11
- FastAPI(api) + beanie(ODM) + fastapi_jwt_auth(authorization)
- MongoDB(DB)
- [File Strorage Adapter](<https://github.com/petrishutin/file_storage_adapter>)

## Run

### run stack locally in docker-compose

``` shellsession
make dev_up
```

### run tests in docker-compose

``` shellsession
make test
```
