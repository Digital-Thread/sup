from apps.feature.domain.value_objects import FeatureId


class FeatureError(Exception):
    pass


class FeatureDoesNotExistError(FeatureError):
    def __init__(self, feature_id: FeatureId, message: str = None):
        self.feature_id = feature_id
        self.message = message or f'Фича с ID {self.feature_id} не найдена.'
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message


class FeatureCreateError(FeatureError):
    def __init__(self, message: str = 'Ошибка при создании фичи'):
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message


class FeatureUpdateError(FeatureError):
    def __init__(self, message: str = 'Ошибка при обновлении фичи'):
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message
