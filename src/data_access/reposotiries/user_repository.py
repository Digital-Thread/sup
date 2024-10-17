import datetime
from typing import List, Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.user.domain.entities import User
from src.apps.user.dtos import UserResponseDTO
from src.apps.user.repositories import IUserRepository
from src.data_access.models import User as UserModel


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.model = UserModel

    async def save(self, user: User) -> None:
        sql_user = UserModel(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=user.password,
            username_tg=user.username_tg,
            nick_tg=user.nick_tg,
            nick_gmeet=user.nick_gmeet,
            nick_gitlab=user.nick_gitlab,
            nick_github=user.nick_github,
            avatar=user.avatar,
            is_superuser=user.is_superuser,
            is_active=user.is_active,
        )
        user._created_at = datetime.datetime.now(datetime.timezone.utc)
        user._updated_at = datetime.datetime.now(datetime.timezone.utc)
        self._session.add(sql_user)
        await self._session.commit()

    async def find_by_email(self, email: str) -> Optional[UserResponseDTO]:
        query = select(self.model).where(self.model.email == email)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def find_all_users(self) -> List[UserResponseDTO]:
        query = select(self.model)
        result = await self._session.execute(query)
        return result.scalars().all()

    async def delete(self, email: str) -> None:
        user = await self.find_by_email(email)
        if user:
            await self._session.delete(user)
            await self._session.commit()

    async def update(self, user: User) -> None:
        query = (
            update(self.model)
            .where(self.model.email == user.email)
            .values(
                first_name=user.first_name,
                last_name=user.last_name,
                is_active=user.is_active,
                is_superuser=user.is_superuser,
                avatar=user.avatar,
                nick_tg=user.nick_tg,
                nick_gmeet=user.nick_gmeet,
                nick_gitlab=user.nick_gitlab,
                nick_github=user.nick_github,
                updated_at=datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None),
            )
        )
        await self._session.execute(query)
        await self._session.commit()
