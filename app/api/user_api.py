from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException

from app.auth_utils import get_current_user_id, hash_password
from app.schemas import User, UserIn

user_router = APIRouter(prefix="/user")


@user_router.post("/")
async def create_user(user_data: UserIn):
    if await User.by_email(user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user_data.password1)
    result = await User.insert_one(User(**user_data.dict(), hashed_password=hashed_password))
    return result.id  # type: ignore


@user_router.get("/", response_model=User)
async def get_user(user_id=Depends(get_current_user_id)):
    user = await User.find_one(User.id == PydanticObjectId(user_id))
    if not user:
        raise HTTPException(status_code=404)
    return user
