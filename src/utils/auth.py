from datetime import datetime, timedelta, timezone
import logging
import traceback
from fastapi import HTTPException, status
from passlib.context import CryptContext
from pydantic import ValidationError
from jose import JWTError, jwt
from sqlmodel import select, Session

from ..schemas.responses.token import TokenPayload
from ..core.settings import settings
from ..models.user import User

logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# pwd_context = CryptContext(schemes=["argon2"], argon2__memory_cost=65536, argon2__time_cost=3, argon2__parallelism=4, argon2__variant="id")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate(session: Session, username: str, password: str):
    user: User = session.exec(
        select(User).where(User.username == username)
    ).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_access_token(data):
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRED)
    raw_data = {**data, "exp": expire}
    return jwt.encode(raw_data, settings.JWT_ACCESS_SECRET_KEY, algorithm=settings.JWT_ACCESS_ALGORITHM)


def create_refresh_token(data):
    expire = datetime.now(timezone.utc) + timedelta(hours=settings.JWT_REFRESH_TOKEN_EXPIRED)
    raw_data = {**data, "exp": expire}
    return jwt.encode(raw_data, settings.JWT_REFRESH_SECRET_KEY, algorithm=settings.JWT_REFRESH_ALGORITHM)


def verify_refresh_token(session: Session, token: str):
    try:
        logger.info("payload")
        payload = jwt.decode(
            token, settings.jwt_refresh_secret_key, algorithms=[settings.JWT_REFRESH_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError) as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user: User = session.query(User).filter(User.username == token_data.sub).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user
