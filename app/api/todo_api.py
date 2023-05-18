from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from app.auth_utils import get_current_user_id
from app.schemas import Todo, TodoEnum, TodoIn

todo_router = APIRouter(prefix="/todo")


def check_todo(todo: Todo | None, user_id: str):
    if not todo:
        raise HTTPException(status_code=404)
    if todo.user_id != user_id:
        raise HTTPException(status_code=403)


@todo_router.post("/")
async def create_todo(todo_data: TodoIn, user_id=Depends(get_current_user_id)):
    result = await Todo.insert_one(Todo(**todo_data.dict(), user_id=user_id))
    return result.id  # type: ignore


@todo_router.get("/")
async def get_todos(user_id=Depends(get_current_user_id)) -> list[Todo]:
    return await Todo.find(Todo.user_id == ObjectId(user_id)).to_list()


@todo_router.get("/{todo_id}")
async def get_todo(todo_id: str, user_id=Depends(get_current_user_id)):
    todo = await Todo.find_one(Todo.id == ObjectId(todo_id))
    check_todo(todo, user_id)
    return todo


@todo_router.put("/{todo_id}")
async def update_todo(todo_id: str, todo_update_data: TodoIn, user_id=Depends(get_current_user_id)):
    todo = await Todo.find_one(Todo.id == ObjectId(todo_id))
    check_todo(todo, user_id)
    return await Todo(**todo_update_data.dict(), user_id=user_id, id=todo_id).save()


@todo_router.patch("/{todo_id}")
async def change_todo_status(todo_id: str, status: TodoEnum, user_id=Depends(get_current_user_id)):
    todo: Todo = await Todo.find_one(Todo.id == ObjectId(todo_id))  # type: ignore
    check_todo(todo, user_id)
    if status is not None and status == todo.status:
        return {"status": todo.status}
    todo.status = status
    await todo.save()
    return {"status": todo.status}


@todo_router.delete("/{todo_id}", status_code=204)
async def delete_todo(todo_id: str, user_id=Depends(get_current_user_id)):  # fmt: skip
    todo: Todo = await Todo.find_one(Todo.id == ObjectId(todo_id))  # type: ignore
    check_todo(todo, user_id)
    await todo.delete()
    return
