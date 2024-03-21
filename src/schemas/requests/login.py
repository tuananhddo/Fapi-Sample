from pydantic import BaseModel, Field

class Login(BaseModel):
    username: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=8)
    