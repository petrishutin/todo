from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext  # type: ignore

from app.auth_utils import create_access_token, hash_password
from app.schemas import Token, User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

auth_router = APIRouter()


@auth_router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await User.by_email(form_data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.hashed_password != hash_password(form_data.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    token = create_access_token({"user_id": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
