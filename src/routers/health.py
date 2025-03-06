import logging
from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel, ValidationError, field_validator, validator

from src.core.settings import settings

from src.exceptions.exceptions import CustomException

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=['health test'])
        
class MyModel(BaseModel):
    value: int

    @field_validator('value')
    @classmethod
    def check_value(cls, v):
        if v < 10:
            raise ValueError("Value must be greater than or equal to 0")
        raise CustomException(name='1')

@router.get("/")
async def root():
    logger.info("This is an info message")
    logger.error("email-validator not installed, email fields will be treated as str.\n"
                "To install, run: pip install email-validator")
    return {"message": "Pong"}

@router.get("/env")
async def envs(param: int):
    return {"message": settings}


@router.post("/vlida")
async def envs(model: MyModel):
    return {"message": settings}


@router.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise CustomException(name=name)
    raise ValidationError("HELPER")
