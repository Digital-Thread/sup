from dataclasses import dataclass


@dataclass
class AccessTokenDTO:
    access_token: str


@dataclass
class RefreshTokenDTO:
    refresh_token: str
