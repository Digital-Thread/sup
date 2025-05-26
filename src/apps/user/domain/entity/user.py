import re
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from src.apps.user.exceptions import (
    InvalidEmailFormatError,
    InvalidNameError,
    MissingDigitError,
    MissingSpecialCharacterError,
    MissingUppercaseLetterError,
    OneOfTheExpire,
    ValidateEmptyLengthError,
    ValidateLengthError,
)


@dataclass
class User:
    first_name: str = field(metadata={'max_length': 20})
    last_name: str = field(metadata={'max_length': 20})
    email: str = field(metadata={'max_length': 50})
    username_tg: str = field(metadata={'max_length': 50})
    nick_tg: str = field(metadata={'max_length': 50})
    nick_gmeet: str = field(metadata={'max_length': 50})
    password: str = field(repr=False)
    nick_gitlab: str = field(default=None, metadata={'max_length': 50})
    nick_github: str = field(default=None, metadata={'max_length': 50})
    avatar: str = field(default=None)
    is_superuser: bool = field(default=False)
    is_active: bool = field(default=False)
    _created_at: datetime = field(default_factory=datetime.now)
    _updated_at: datetime = field(default_factory=datetime.now)
    _id: UUID = field(default_factory=uuid4)

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @property
    def id(self) -> UUID:
        return self._id

    def __post_init__(self) -> None:
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        self.email = self.email.lower()
        self.validate_all_fields()
        self.validate_password(password=self.password)

    def validate_all_fields(self) -> None:
        for field_name in [
            'first_name',
            'last_name',
            'email',
            'username_tg',
            'nick_tg',
            'nick_gmeet',
        ]:
            value = getattr(self, field_name)
            self.validate_length(value, field_name)

            if field_name in ['first_name', 'last_name']:
                self.validate_name(value)
            if field_name in ['email']:
                self.validate_email(value)

        if not (self.nick_gitlab or self.nick_github):
            raise OneOfTheExpire()

        if self.nick_gitlab:
            self.validate_length(self.nick_gitlab, 'nick_gitlab')
        if self.nick_github:
            self.validate_length(self.nick_github, 'nick_github')

    def validate_length(self, value: str, field_name: str) -> None:
        if value is None or value.strip() == '':
            raise ValidateEmptyLengthError(field_name)
        max_length = self.__dataclass_fields__[field_name].metadata['max_length']
        if len(value) > max_length:
            raise ValidateLengthError(field_name, max_length)

    @staticmethod
    def validate_name(name: str) -> None:
        pattern = r'^[a-zA-Zа-яА-ЯёЁ]+$'
        if not re.match(pattern, name):
            raise InvalidNameError()

    @staticmethod
    def validate_email(email: str) -> None:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            raise InvalidEmailFormatError()

    @staticmethod
    def validate_password(password: str) -> str | None:
        if password is None:
            return password
        if not re.search(r'[A-Z]', password):
            raise MissingUppercaseLetterError()
        if not re.search(r'\d', password):
            raise MissingDigitError()
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise MissingSpecialCharacterError()
        return password
