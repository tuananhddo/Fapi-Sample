from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import APIKeyHeader, APIKeyQuery, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from src.dependencies import SessionDep
from src.schemas.responses.token import Token
from src.settings import settings
from src.utils import auth

# to get a string like this run:
# openssl rand -hex 32

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
# 
router = APIRouter(prefix="/auth")


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str



def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not auth.verify_password(password, user.hashed_password):
        return False
    return user


@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep
) -> Token:
    print(form_data.username)
    user = auth.authenticate(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token = auth.create_access_token(
        {"sub": user.username},
    )
    refresh_token = auth.create_refresh_token(
        data={"sub": user.username},
    )
    return Token(access_token=access_token, refresh_token=refresh_token)


# @router.get("/users/me/", response_model=User)
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_active_user)]
# ):
#     return current_user

