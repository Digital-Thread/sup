from abc import ABC, abstractmethod
from typing import Any

from src.apps.feature.repositories import IFeatureRepository


class BaseInteractor(ABC):
    def __init__(self, feature_repository: IFeatureRepository):
        self._repository = feature_repository

    @abstractmethod
    async def execute(self, *args: Any) -> Any: ...
