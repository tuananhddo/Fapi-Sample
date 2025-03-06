from typing import Optional

from src.models.base import BaseModel
from sqlmodel import Field, Relationship


class Item(BaseModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str
    owner_id: int = Field(foreign_key="user.id")
    owner: Optional["User"] = Relationship(back_populates="items")
