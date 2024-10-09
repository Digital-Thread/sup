from typing import Any, Type, TypeVar

T = TypeVar('T', bound='BaseDTO')


class BaseDTO:
    @classmethod
    def from_entity(cls: Type[T], entity: Any) -> T:
        """Метод для создания DTO из сущности."""
        entity_dict = entity.__dict__

        # Удаляем модификатор доступа _ из ключей, так как в dto их нет
        dto_dict = {key.lstrip('_'): value for key, value in entity_dict.items()}

        return cls(**dto_dict)
