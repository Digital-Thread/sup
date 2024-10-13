from pydantic import BaseModel


class ClientAccessTokenDTO(BaseModel):
    client_access_token: str


class ClientRefreshTokenDTO(BaseModel):
    client_refresh_token: str


class ServerAccessTokenDTO(BaseModel):
    server_access_token: str


class ServerRefreshTokenDTO(BaseModel):
    server_refresh_token: str
