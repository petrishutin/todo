from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException
from app.schemas import Todo, TodoIn, User, UserIn

api_router = APIRouter(prefix="/api/v1")


@api_router.post("/user", tags=["Users"])
async def create_user(user_data: UserIn):
    result = await User.insert_one(User(**user_data.dict(), hashed_password=user_data.password1))
    return result.id  # type: ignore


@api_router.get("/user/{user_id}", response_model=User, tags=["Users"])
async def get_user(user_id: str):
    return await User.find_one(User.id == PydanticObjectId(user_id))


@api_router.post("/user/{user_id}/todo", tags=["ToDos"])
async def create_todo(user_id: str, todo_data: TodoIn):
    result = await Todo.insert_one(Todo(**todo_data.dict(), user_id=user_id))
    return result.id  # type: ignore


@api_router.get("/user/{user_id}/todo", tags=["ToDos"])
async def get_todos(user_id: str) -> list[Todo]:
    return await Todo.find(Todo.user_id == user_id).to_list()


@api_router.get("/user/{user_id}/todo/{todo_id}", tags=["ToDos"])
async def get_todo(user_id: str, todo_id: str):
    todo = await Todo.find_one(Todo.id == todo_id and Todo.user_id == user_id)
    if not todo:
        raise HTTPException(status_code=404)
    return todo


@api_router.put("/user/{user_id}/todo/{todo_id}", tags=["ToDos"])
async def update_todo(user_id: str, todo_id: str, todo_update_data: TodoIn):
    todo = await Todo.find_one(Todo.id == todo_id and Todo.user_id == user_id)
    if not todo:
        raise HTTPException(status_code=404)
    return await Todo(**todo_update_data.dict(), user_id=user_id, id=todo_id).save()


@api_router.delete("/user/{user_id}/todo/{todo_id}", tags=["ToDos"])
async def delete_todo(user_id: str, todo_id: str,):  # fmt: skip
    todo = await Todo.find(Todo.id == todo_id and Todo.user_id == user_id).first_or_none()
    if not todo:
        raise HTTPException(status_code=404)
    await todo.delete()
    return
