from src.apps.user.domain.entities import User
from src.data_access.models import UserModel


class UserMapper:

    @staticmethod
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
            id=user.id,
        )

    @staticmethod
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
            _id=user_model.id,
        )