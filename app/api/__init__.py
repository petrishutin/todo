from fastapi import APIRouter

from app.api.attachments_api import attachments_router
from app.api.auth_api import auth_router
from app.api.todo_api import todo_router
from app.api.user_api import user_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(todo_router, tags=["ToDos"])
api_router.include_router(user_router, tags=["Users"])
api_router.include_router(auth_router, tags=["Auth"])
api_router.include_router(attachments_router, tags=["Attachments"])
