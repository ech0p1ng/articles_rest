from typing import Any
from fastapi import HTTPException


class NotFoundError(HTTPException):
    status_code = 404

    def __init__(
        self,
        entity_name: str,
        filter: dict[str, Any] | None = None
    ) -> None:
        '''
        Ошибка, возникающая когда что-то не найдено

        Args:
            entity_name (str): Название сущности на английском \
                со строчной буквы
            filter (dict[str, Any] | None, optional): Фильтр, по которому \
                не удалось найти сущность. Defaults to None.
        '''
        detail = f'Не найдена сущность "{entity_name}"'
        if filter:
            detail += f' по фильтру {filter}'

        super().__init__(self.status_code, detail)


class AlreadyExistsError(HTTPException):
    status_code = 403

    def __init__(
        self,
        entity_name: str,
        filter: dict[str, Any] | None = None
    ) -> None:
        detail = f'Сущность "{entity_name}"'
        if filter:
            detail += f' с {filter}'
        detail += ' уже существует'

        super().__init__(self.status_code, detail)


class RedisError(HTTPException):
    status_code = 500

    def __init__(
        self,
        detail: Any
    ) -> None:
        super().__init__(self.status_code, detail)
