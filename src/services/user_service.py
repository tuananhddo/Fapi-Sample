from sqlmodel import Session, select
from sqlalchemy import or_

from ..exceptions.exceptions import DuplicateData
from ..schemas import base as schemas
from ..models.user import User
from ..models.item import Item


def check_user_not_exist(db: Session, rq: schemas.UserCreate):
    user = db.query(User).filter(or_(User.email == rq.email, User.username == rq.username)).first()
    if user:
        raise DuplicateData(identity_field="Email, Username", message_template="{} already registered")
    return user

def get_user(db: Session, user_id: int):
    return db.exec(
        select(User).where(User.id == user_id)
    ).first()


def get_user_by_email(db: Session, email: str):
    return db.exec(
        select(User).where(User.email == email)
    ).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = Item(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item