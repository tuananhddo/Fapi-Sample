from pydantic import BaseModel


class LoginToken(BaseModel):
    access_token: str
    refresh_token: str

class AccessToken(BaseModel):
    access_token: str

class RefreshToken(BaseModel):
    refresh_token: str

class TokenPayload(BaseModel):
    sub: str | None = None
    exp: int