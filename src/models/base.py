from sqlalchemy import Boolean, Column, String, DateTime, func
from ..core.database import Base


class BaseModel(Base):

    __abstract__ = True

    created_at = Column(DateTime, default=func.now())
    created_by = Column(String)

    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_by = Column(String)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}