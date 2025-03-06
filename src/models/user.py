from sqlmodel import Field, Relationship
from src.models.base import BaseModel


class User(BaseModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    name: str = Field(index=True)
    password: str = Field()
    is_active: bool = Field(default=True)
    items: list["Item"] = Relationship(back_populates="owner")
