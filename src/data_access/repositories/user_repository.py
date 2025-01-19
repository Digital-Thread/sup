import datetime
from typing import List, Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.user.domain.entities import User
from src.apps.user.repositories import IUserRepository
from src.data_access.mappers.user_mapper import UserMapper
from src.data_access.models import UserModel


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.model = UserModel

    async def save(self, user: User) -> None:
        stmt = UserMapper.domain_to_model(user)
        user._created_at = datetime.datetime.now(datetime.timezone.utc)
        user._updated_at = datetime.datetime.now(datetime.timezone.utc)
        self._session.add(stmt)

    async def find_by_email(self, email: str) -> Optional[User]:
        query = select(self.model).where(self.model.email == email.lower())
        result = await self._session.execute(query)
        sql_user = result.scalar_one_or_none()
        return UserMapper.model_to_domain(sql_user) if sql_user else None

    async def find_all_users(
        self, limit: int, offset: int, sort_by: Optional[str] = None, sort_order: str = 'asc'
    ) -> List[User]:
        query = select(self.model)
        if sort_by:
            sort_column = getattr(self.model, sort_by, None)
            if sort_column:
                if sort_order == 'desc':
                    query = query.order_by(sort_column.desc())
                else:
                    query = query.order_by(sort_column.asc())
        query = query.offset(offset).limit(limit)
        result = await self._session.execute(query)
        sql_users = result.scalars().all()
        return [UserMapper.model_to_domain(sql_user) for sql_user in sql_users]

    async def delete(self, email: str) -> None:
        stmt = select(self.model).where(self.model.email == email)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            await self._session.delete(model)

    async def update(self, user: User) -> None:
        stmt = (
            update(self.model)
            .where(self.model.email == user.email)
            .values(
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                password=user.password,
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
        await self._session.execute(stmt)
