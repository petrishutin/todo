from datetime import datetime, timedelta

import bcrypt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt  # type: ignore
from passlib.context import CryptContext  # type: ignore

from app.settings import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


def hash_password(password: str) -> str:
    """Returns a salted password hash"""
    settings = get_settings()
    return bcrypt.hashpw(password.encode("utf-8"), settings.SALT.encode()).decode()


def create_access_token(data: dict):
    settings = get_settings()
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRATION_TIME)})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


def get_current_user_id(token: str = Depends(oauth2_scheme)):
    settings = get_settings()
    return jwt.decode(token, settings.SECRET_KEY, algorithms="HS256").get("user_id")
