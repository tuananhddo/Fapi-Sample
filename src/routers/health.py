from typing import Annotated
from fastapi import APIRouter, Depends, Header

from src import settings
from src.database import SessionLocal
from src.utils.auth import get_password_hash
from sqlalchemy.orm import Session


router = APIRouter(prefix="/hth", tags=['health test'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.get("/ping")
async def root():
    return {"message": "Pong"}

@router.get("/env")
async def envs(user_agent: Annotated[str | None, Header()]):
    print(get_password_hash("test"))
    return {"message": settings}

@router.get("/db")
async def test_tnx(db: Session = Depends(get_db)):
    return {"message": "Pong"}


