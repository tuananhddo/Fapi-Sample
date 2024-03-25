from pydantic import BaseModel


class ResponseUser(BaseModel):
    id: int
    is_active: bool
    username: str