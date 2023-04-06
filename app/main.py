from api import api_router
from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from schemas import Todo, User

app = FastAPI()

app.include_router(api_router)


@app.on_event("startup")
async def start_db():
    client = AsyncIOMotorClient("mongodb://test:test@localhost:27017/")
    await init_beanie(database=client.db_name, document_models=[User, Todo])
