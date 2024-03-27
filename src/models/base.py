from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from ..core.database import Base


class BaseModel(Base):
    created_at = Column(DateTime, default=func.now())
    created_by = Column(String)

    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_by = Column(String)