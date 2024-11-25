from re import match


class NameValidatorMixin:

    @staticmethod
    def _is_valid_name(name: str, entity_name: str) -> None:
        if not name.strip():
            raise ValueError(f'Имя {entity_name} должно содержать хотя бы одну букву')

        pattern = r'^[a-zA-Zа-яА-ЯёЁ\s]{1,20}$'
        if not bool(match(pattern, name)):

            if len(name) > 20:
                raise ValueError(
                    f'Длина названия {entity_name} не должна превышать 20 символов включая пробелы'
                )

            raise ValueError(f'Неверный формат названия {entity_name}')


class DescriptionValidatorMixin:

    @staticmethod
    def _is_valid_description(description: str, entity_name: str) -> None:
        pattern = r'^[a-zA-Zа-яА-ЯёЁ\s\.\-]{1,500}$'
        if not bool(match(pattern, description)):
            raise ValueError(
                f'Длина описания {entity_name} не должна превышать 500 символов.'
                f'И содержать только буквы латинского и русского алфавитов, включая символы пробела и -.'
            )


class ColorValidatorMixin:

    @staticmethod
    def _is_valid_color(color: str) -> None:
        pattern = r'^#[A-Fa-f0-9]{6}$'
        if not bool(match(pattern, color)):
            raise ValueError(f'Неверный формат цвета {color}')
