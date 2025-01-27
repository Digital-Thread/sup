from dataclasses import dataclass


@dataclass
class UserCreateDTO:
    first_name: str
    last_name: str
    email: str
    username_tg: str
    nick_tg: str
    nick_gmeet: str
    nick_gitlab: str | None = None
    nick_github: str | None = None
    avatar: str | None = None
    password: str = None


@dataclass
class AdminCreateUserDTO(UserCreateDTO):
    is_active: bool | None = False
    send_mail: bool | None = False


@dataclass
class UserUpdateDTO:
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    username_tg: str | None = None
    nick_tg: str | None = None
    nick_gmeet: str | None = None
    nick_gitlab: str | None = None
    nick_github: str | None = None
    avatar: str | None = None


@dataclass
class UserPasswordUpdateDTO:
    plain_password: str | None = None
    new_password: str | None = None


@dataclass
class AdminPasswordUpdateDTO:
    new_password: str | None = None


@dataclass
class AuthDTO:
    email: str
    password: str
