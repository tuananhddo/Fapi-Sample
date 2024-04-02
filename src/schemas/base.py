from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator


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
    email: str
    username: str
    name: str

class UserCreate(UserBase):
    password: str = Field(min_length=4)

    @field_validator('username', 'password')
    @classmethod
    def check_strong(cls, v: str, info: ValidationInfo) -> str:
        print('1')
        return v

class UserUpdate(BaseModel):
    name: str

class User(UserBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
