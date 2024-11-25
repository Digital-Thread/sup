from typing import Any, Tuple

from src.apps import ApplicationException
from src.apps.feature.domain import FeatureId


class FeatureError(ApplicationException):
    DEFAULT_MESSAGE = 'Ошибка во время работы с фичёй.'

    def __init__(self, context: Exception = None, message: str = None) -> None:
        self.context = context
        self.message = message or self.DEFAULT_MESSAGE
        self.args: Tuple[Any, ...] = (self.context, self.message)

    def __str__(self) -> str:
        if self.context:
            return f'{self.message} {self.context}'

        return self.message


class FeatureCreateError(FeatureError):
    DEFAULT_MESSAGE = 'Ошибка во время создания фичи.'


class FeatureUpdateError(FeatureError):
    DEFAULT_MESSAGE = 'Ошибка при обновлении фичи.'


class FeatureDeleteError(FeatureError):
    DEFAULT_MESSAGE = 'Ошибка во время удаления фичи.'


class FeatureDoesNotExistError(FeatureError):
    DEFAULT_MESSAGE = 'Фича не найдена.'

    def __init__(
        self, feature_id: FeatureId = None, context: Exception = None, message: str = None
    ) -> None:
        custom_message = f'Фича с ID {feature_id} не найдена.' if feature_id else message
        super().__init__(context=context, message=custom_message or self.DEFAULT_MESSAGE)
        self.feature_id = feature_id
        self.args = (self.feature_id, self.context, self.message)


class FeatureRepositoryError(FeatureError):
    DEFAULT_MESSAGE = 'Ошибка репозитория.'
