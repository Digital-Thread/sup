import datetime
from typing import List, Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.user.domain.entities import User
from src.apps.user.repositories import IUserRepository
from src.data_access.models import User as UserModel


def domain_to_model(user: User) -> UserModel:
    return UserModel(
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
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


def model_to_domain(user_model: UserModel) -> User:
    return User(
        first_name=user_model.first_name,
        last_name=user_model.last_name,
        email=user_model.email,
        password=user_model.password,
        username_tg=user_model.username_tg,
        nick_tg=user_model.nick_tg,
        nick_gmeet=user_model.nick_gmeet,
        nick_gitlab=user_model.nick_gitlab,
        nick_github=user_model.nick_github,
        avatar=user_model.avatar,
        is_superuser=user_model.is_superuser,
        is_active=user_model.is_active,
        _created_at=user_model.created_at,
        _updated_at=user_model.updated_at,
    )


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.model = UserModel

    async def save(self, user: User) -> None:
        sql_user = domain_to_model(user)
        user._created_at = datetime.datetime.now(datetime.timezone.utc)
        user._updated_at = datetime.datetime.now(datetime.timezone.utc)
        self._session.add(sql_user)
        await self._session.commit()

    async def find_by_email(self, email: str) -> Optional[User]:
        query = select(self.model).where(self.model.email == email)
        result = await self._session.execute(query)
        sql_user = result.scalar_one_or_none()
        return model_to_domain(sql_user) if sql_user else None

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
        return [model_to_domain(sql_user) for sql_user in sql_users]

    async def delete(self, email: str) -> None:
        query = select(self.model).where(self.model.email == email)
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.commit()

    async def update(self, user: User) -> None:
        query = (
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
        await self._session.execute(query)
        await self._session.commit()
