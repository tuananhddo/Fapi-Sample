from fastapi import APIRouter, Depends, HTTPException

from src.dependencies import SessionDep
from ..schemas import base as schemas
from src import crud
from src.database import SessionLocal
from sqlalchemy.orm import Session
from src.utils import auth

router = APIRouter(prefix="/users", tags=['users'])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: SessionDep):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.password = auth.get_password_hash(user.password)
    return crud.create_user(db=db, user=user)


@router.get("/users/", response_model=list[schemas.User])
def read_users(db: SessionDep, skip: int = 0, limit: int = 100):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: SessionDep):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: SessionDep
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@router.get("/items/", response_model=list[schemas.Item])
def read_items(db: SessionDep, skip: int = 0, limit: int = 100):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items