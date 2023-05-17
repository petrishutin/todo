from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT  # type: ignore

from app.schemas import User, UserAuth
from app.sec_utils import hash_password
from app.settings import Settings

auth_router = APIRouter(prefix="/auth")


@AuthJWT.load_config
def get_config():
    return Settings()


@auth_router.post("/login")
async def login(user: UserAuth, auth: AuthJWT = Depends()):
    user_in_db = await User.by_email(user.email)
    if user is None or user_in_db.hashed_password != hash_password(user.password):
        raise HTTPException(status_code=401, detail="Bad email or password")
    access_token = auth.create_access_token(subject=user.email)
    return {"access_token": access_token}


@auth_router.post("/logout")
async def logout(auth: AuthJWT = Depends()):
    auth.jwt_required()
    auth.unset_jwt_cookies()
    return {"message": "Successfully logged out"}
