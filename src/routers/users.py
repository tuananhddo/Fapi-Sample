import logging

from fastapi import APIRouter, Depends, HTTPException

from src import models
from src.dependencies import CurrentUser, SessionDep
from src.exceptions.exceptions import DataNotFound, DuplicateData
from ..schemas import base as schemas
from src.services import user_service
from src.utils import auth

router = APIRouter(prefix="/users", tags=['users'])
logger = logging.getLogger(__name__)


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: SessionDep):
    user.password = auth.get_password_hash(user.password)
    user_service.check_user_not_exist(db, user)
    return user_service.create_user(db=db, user=user)

@router.put("/", response_model=schemas.User)
def update_user(current_user: CurrentUser, update_model: schemas.UserUpdate, session: SessionDep):
    logger.info("Update")

    current_user.name = update_model.name
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user

@router.get("/", response_model=list[schemas.User])
def read_users(db: SessionDep, skip: int = 0, limit: int = 100):
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: SessionDep):
    db_user = user_service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: SessionDep
):
    return user_service.create_user_item(db=db, item=item, user_id=user_id)


@router.get("/items/", response_model=list[schemas.Item])
def read_items(db: SessionDep, skip: int = 0, limit: int = 100):
    items = user_service.get_items(db, skip=skip, limit=limit)
    return items