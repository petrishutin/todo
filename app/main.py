from beanie import init_beanie
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from motor.motor_asyncio import AsyncIOMotorClient
from app.schemas import Todo, User
from app.settings import settings
from app.api import api_router

app = FastAPI()

app.include_router(api_router)


@app.on_event("startup")
async def start_db():
    client = AsyncIOMotorClient(settings.MONGO_URI)
    await init_beanie(database=client.db_name, document_models=[User, Todo])


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):  # noqa F811
    return JSONResponse(
        status_code=exc.status_code,  # type: ignore
        content={"detail": exc.message}  # type: ignore
    )
