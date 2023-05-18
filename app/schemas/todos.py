from enum import Enum

from beanie import Document
from pydantic import BaseModel

from app.schemas.attachments import Attachment


class TodoEnum(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TodoIn(BaseModel):
    title: str
    description: str
    status: TodoEnum
    attachments: list[Attachment] = []


class Todo(Document):
    user_id: str
    title: str
    description: str
    status: TodoEnum
    attachments: list[Attachment] = []

    class Settings:
        name = "Todos"
