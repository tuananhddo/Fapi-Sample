from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import APIKeyHeader, APIKeyQuery, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from src.dependencies import SessionDep, get_current_active_superuser, get_current_user
from src.models.user import User
from src.schemas.responses.token import AccessToken, LoginToken, RefreshToken
from src.schemas.responses.user import ResponseUser
from src.core.settings import settings
from src.utils import auth

# to get a string like this run:
# openssl rand -hex 32

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
# 
router = APIRouter(prefix="/auth", tags=['auth'])


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep
) -> LoginToken:
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
    return LoginToken(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh")
async def refresh(
    data: RefreshToken,
    session: SessionDep
) -> AccessToken:
    user: User = auth.verify_refresh_token(session, data.refresh_token)
    access_token = auth.create_access_token(
        {"sub": user.username},
    )
    return AccessToken(access_token=access_token)

@router.get("/me", response_model=ResponseUser)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return ResponseUser(**current_user.to_dict())

