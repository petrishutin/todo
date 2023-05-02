from enum import Enum

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, EmailStr, validator
from fastapi import UploadFile


class TodoEnum(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TodoIn(BaseModel):
    title: str
    description: str
    status: TodoEnum


class Todo(Document):
    user_id: str
    title: str
    description: str
    status: TodoEnum

    class Settings:
        name = "Todos"
