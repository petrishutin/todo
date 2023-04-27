from enum import Enum

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, EmailStr, validator


class TodoEnum(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class UserIn(BaseModel):
    name: str
    email: EmailStr
    password1: str
    password2: str

    @validator("password1")
    def passwords_match(cls, v, values, **kwargs):
        if "password2" in values and v != values["password2"]:
            raise ValueError("passwords do not match")
        return v


class UserAuth(BaseModel):
    """User register and login auth"""
    email: EmailStr
    password: str


class User(Document):
    _id: PydanticObjectId
    name: str
    email: EmailStr
    hashed_password: str

    class Settings:
        name = "Users"

    @classmethod
    async def by_email(cls, email: str):
        """Get a user by email"""
        return await cls.find_one(cls.email == email)


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
