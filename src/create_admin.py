import asyncio

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from data_access.repositories.user_repository import UserRepository
from src.data_access.models.user import UserModel as User
from src.providers.adapters import ConfigProvider

config = ConfigProvider().provide_config()
DATABASE_URL = config.db.construct_sqlalchemy_url

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class CreateUserAdmin:
    def __init__(self, repository: UserRepository, pwd_context: CryptContext):
        self.repository = repository
        self.pwd_context = pwd_context

    async def check_user(self, email: str) -> bool:
        user = await self.repository.find_by_email(email=email)
        if user:
            print('Такой пользователь уже существует.')
            return False
        return True

    async def create_user(self, email: str, password: str) -> None:
        hash_password = self.pwd_context.hash(password)
        new_user = User(
            email=email,
            is_superuser=True,
            is_active=True,
            password=hash_password,
            first_name='',
            last_name='',
            username_tg='',
            nick_tg='',
            nick_gmeet='',
            nick_gitlab='',
            nick_github='',
            avatar='',
        )
        await self.repository.save(user=new_user)
        print('Администратор успешно создан.')


async def main() -> None:
    async with AsyncSessionLocal() as session:
        user_repository = UserRepository(session)
        pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        create_user_admin = CreateUserAdmin(user_repository, pwd_context)

        while True:
            email = input('Введите email: ')
            user_exists = await create_user_admin.check_user(email)
            if not user_exists:
                return

            password1 = input('Введите пароль: ')
            password2 = input('Повторите пароль: ')

            if password1 != password2:
                print('Пароли не совпадают. Пожалуйста, попробуйте снова.')
                continue

            await create_user_admin.create_user(email, password1)
            break


if __name__ == '__main__':
    asyncio.run(main())
