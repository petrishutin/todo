from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt  # type: ignore
from passlib.context import CryptContext  # type: ignore

from app.schemas import Token, User
from app.sec_utils import hash_password
from app.settings import get_settings

SECRET_KEY = "61ab2f50c65f2d1ddc99ea0cbacab9332c3e5acd6fa8dedf5d35e79c68fd5bb5"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")

auth_router = APIRouter()


def create_access_token(data: dict):
    settings = get_settings()
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRATION_TIME)})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


def get_current_user_id(token: str = Depends(oauth2_scheme)):
    return jwt.decode(token, SECRET_KEY, algorithms="HS256").get("user_id")


@auth_router.post("/login", response_model=Token)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    if not (user := await User.by_email(form_data.username)):
        raise HTTPException(status_code=404, detail="User not found")
    if user["hashed_password"] != hash_password(form_data.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    response.set_cookie(key="access_token", value=create_access_token(user["id"]), httponly=True)
    return {"message": "success"}
