from enum import Enum

from beanie import Document
from pydantic import BaseModel


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
