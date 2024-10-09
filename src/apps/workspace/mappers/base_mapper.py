class BaseMapper[E, DTO]:
    @staticmethod
    def entity_to_dto(entity: E, dto_class: type) -> DTO:
        entity_dict = entity.__dict__

        # Удаляем модификатор доступа _ из ключей, так как в dto их нет
        dto_dict = {key.lstrip('_'): value for key, value in entity_dict.items()}
        return dto_class(**dto_dict)
