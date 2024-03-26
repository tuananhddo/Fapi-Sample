import logging
from typing import Annotated
from fastapi import APIRouter, Depends, Header

from src import settings
from src.database import SessionLocal
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/hth", tags=['health test'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.get("/ping")
async def root():
    # logging.info("This is an info message")
    logger.warning("email-validator not installed, email fields will be treated as str.\n"
                "To install, run: pip install email-validator")
    return {"message": "Pong"}

@router.get("/env")
async def envs(user_agent: Annotated[str | None, Header()]):
    return {"message": settings}

@router.get("/db")
async def test_tnx(db: Session = Depends(get_db)):
    return {"message": "Pong"}


