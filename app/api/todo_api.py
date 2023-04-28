from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException

from app.schemas import Todo, TodoIn, User, UserIn

todo_router = APIRouter(prefix="/user")


@todo_router.post("/{user_id}/todo")
async def create_todo(user_id: str, todo_data: TodoIn):
    result = await Todo.insert_one(Todo(**todo_data.dict(), user_id=user_id))
    return result.id  # type: ignore


@todo_router.get("/{user_id}/todo")
async def get_todos(user_id: str) -> list[Todo]:
    return await Todo.find(Todo.user_id == user_id).to_list()


@todo_router.get("/{user_id}/todo/{todo_id}")
async def get_todo(user_id: str, todo_id: str):
    todo = await Todo.find_one(Todo.id == todo_id and Todo.user_id == user_id)
    if not todo:
        raise HTTPException(status_code=404)
    return todo


@todo_router.put("/{user_id}/todo/{todo_id}")
async def update_todo(user_id: str, todo_id: str, todo_update_data: TodoIn):
    todo = await Todo.find_one(Todo.id == todo_id and Todo.user_id == user_id)
    if not todo:
        raise HTTPException(status_code=404)
    return await Todo(**todo_update_data.dict(), user_id=user_id, id=todo_id).save()


@todo_router.delete("/{user_id}/todo/{todo_id}")
async def delete_todo(user_id: str, todo_id: str,):  # fmt: skip
    todo = await Todo.find(Todo.id == todo_id and Todo.user_id == user_id).first_or_none()
    if not todo:
        raise HTTPException(status_code=404)
    await todo.delete()
    return
