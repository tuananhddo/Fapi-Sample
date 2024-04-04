from typing import Annotated
from pydantic import AfterValidator, BaseModel, ConfigDict, EmailStr, Field, ValidationError, ValidationInfo, field_validator, model_validator

from src.utils.string import check_special_characters, check_strong_password

Password = Annotated[str, AfterValidator(check_strong_password)]

class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    email: EmailStr
    username: str
    name: str

class UserCreate(UserBase):
    password: Password

    @field_validator('username')
    @classmethod
    def check_strong(cls, v: str, info: ValidationInfo) -> str:
        check_special_characters(v)
        return v
    
    @model_validator(mode='after')
    def check_complex(self) -> "UserCreate":
        pwd = self.password
        usn = self.username
        if pwd in usn or usn in pwd:
            raise ValueError("Username and password too similar")
        return self
    
class UserUpdate(BaseModel):
    name: str

class User(UserBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
