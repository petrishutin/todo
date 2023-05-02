from beanie import init_beanie
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException  # type: ignore
from motor.motor_asyncio import AsyncIOMotorClient

from app.api import api_router
from app.schemas import Attachment, Todo, User
from app.settings import Settings

app = FastAPI()

app.include_router(api_router)


def get_settings():
    return Settings()


@app.on_event("startup")
async def start_db():
    settings = get_settings()
    client = AsyncIOMotorClient(settings.MONGO_URI)
    await init_beanie(database=client.db_name, document_models=[User, Todo, Attachment])


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):  # noqa F811
    return JSONResponse(
        status_code=exc.status_code,  # type: ignore
        content={"detail": exc.message},  # type: ignore
    )
