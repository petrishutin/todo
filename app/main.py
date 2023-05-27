from beanie import init_beanie
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from jose import JWTError  # type: ignore
from motor.motor_asyncio import AsyncIOMotorClient

from app.api import api_router
from app.schemas import Attachment, Todo, User
from app.settings import Settings

app = FastAPI(title="Todo API", version="0.1.0")

app.include_router(api_router)

origins = ["http://localhost:8080", "http://localhost", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_settings():
    return Settings()


@app.on_event("startup")
async def start_db():
    settings = get_settings()
    client = AsyncIOMotorClient(settings.MONGO_URI)
    await init_beanie(database=client.todos, document_models=[User, Todo, Attachment])


@app.exception_handler(JWTError)
def jwt_exception_handler(request: Request, exc: JWTError):  # noqa F811
    return JSONResponse(
        status_code=exc.status_code,  # type: ignore
        content={"detail": exc.message},  # type: ignore
    )
