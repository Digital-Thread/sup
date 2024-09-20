import datetime
import hashlib
import uuid
import re
from dataclasses import dataclass, field


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
    _created_at: datetime.datetime = field(default_factory=datetime.datetime.now)
    _updated_at: datetime.datetime = field(default_factory=datetime.datetime.now)
    _id: uuid.UUID = field(default_factory=uuid.uuid4)

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @property
    def id(self) -> uuid:
        return self._id

    def __post_init__(self):
        self.password = self._hash_password(self.password)
        self._validate_all_fields()

    def _validate_all_fields(self) -> None:
        for field_name in ['first_name', 'last_name', 'email', 'username_tg', 'nick_tg', 'nick_gmeet']:
            value = getattr(self, field_name)
            self._validate_length(value, field_name)
            if field_name in ['first_name', 'last_name']:
                self._validate_name(value)
        self._validate_email(self.email)

        if not (self.nick_gitlab or self.nick_github):
            raise ValueError('Необходимо указать хотя бы один ник: nick_gitlab или nick_github.')

        if self.nick_gitlab:
            self._validate_length(self.nick_gitlab, 'nick_gitlab')
        if self.nick_github:
            self._validate_length(self.nick_github, 'nick_github')

    def _validate_length(self, value: str, field_name: str) -> None:
        if value is None or value.strip() == "":
            raise ValueError(f'{field_name} не может быть пустым.')
        max_length = self.__dataclass_fields__[field_name].metadata['max_length']
        if len(value) > max_length:
            raise ValueError(f'Длина {field_name} не должна превышать {max_length} символов.')

    @staticmethod
    def _validate_name(name: str) -> None:
        pattern = r'^[a-zA-Zа-яА-ЯёЁ]+$'
        if not re.match(pattern, name):
            raise ValueError(
                'В названии допускается использование только букв латинского и кириллического алфавитов.'
            )

    @staticmethod
    def _validate_email(email: str) -> None:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            raise ValueError('Некорректный формат электронной почты.')

    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()