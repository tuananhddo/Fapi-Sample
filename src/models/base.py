from typing import Optional

from sqlmodel import Field, SQLModel
from datetime import datetime
from sqlalchemy import func, text, TIMESTAMP


class BaseModel(SQLModel):

    created_at: datetime = Field(
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")},
        nullable=False
    )

    updated_at: Optional[datetime] = Field(
        default=None,
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={"onupdate": func.now(), "nullable": True}
    )
    created_by: str | None = None
    updated_by: str | None = None


    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}