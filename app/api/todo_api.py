from fastapi import APIRouter, Depends, HTTPException

from app.auth_utils import get_current_user_id
from app.schemas import Todo, TodoIn

todo_router = APIRouter(prefix="/todo")


@todo_router.post("/")
async def create_todo(todo_data: TodoIn, user_id=Depends(get_current_user_id)):
    result = await Todo.insert_one(Todo(**todo_data.dict(), user_id=user_id))
    return result.id  # type: ignore


@todo_router.get("/")
async def get_todos(user_id=Depends(get_current_user_id)) -> list[Todo]:
    return await Todo.find(Todo.user_id == user_id).to_list()


@todo_router.get("/{todo_id}")
async def get_todo(todo_id: str, user_id=Depends(get_current_user_id)):
    todo = await Todo.find_one(Todo.id == todo_id and Todo.user_id == user_id)
    if not todo:
        raise HTTPException(status_code=404)
    return todo


@todo_router.put("/{todo_id}")
async def update_todo(todo_id: str, todo_update_data: TodoIn, user_id=Depends(get_current_user_id)):
    todo = await Todo.find_one(Todo.id == todo_id and Todo.user_id == user_id)
    if not todo:
        raise HTTPException(status_code=404)
    return await Todo(**todo_update_data.dict(), user_id=user_id, id=todo_id).save()


@todo_router.delete("/{todo_id}")
async def delete_todo(todo_id: str, user_id=Depends(get_current_user_id)):  # fmt: skip
    todo = await Todo.find(Todo.id == todo_id and Todo.user_id == user_id).first_or_none()
    if not todo:
        raise HTTPException(status_code=404)
    await todo.delete()
    return
