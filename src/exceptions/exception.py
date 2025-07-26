from typing import Any
from fastapi import HTTPException


class NotFoundError(HTTPException):
    def __init__(
        self,
        entity_name: str,
        filter: dict[str, Any] | None = None
    ) -> None:
        status_code = 404
        detail = f'Не найдена сущность "{entity_name}"'
        if filter:
            detail += f' по фильтру {filter}'

        super().__init__(status_code, detail)


class AlreadyExistsError(HTTPException):
    def __init__(
        self,
        entity_name: str,
        filter: dict[str, Any] | None = None
    ) -> None:
        status_code = 403
        detail = f'Сущность "{entity_name}"'
        if filter:
            detail += f' с {filter}'
        detail += ' уже существует'

        super().__init__(status_code, detail)
