from pydantic import BaseModel


class AccessTokenDTO(BaseModel):
    access_token: str


class RefreshTokenDTO(BaseModel):
    refresh_token: str
