from typing import Any
from fastapi import HTTPException


class NotFoundError(HTTPException):
    def __init__(self, entity_name: str, filter: dict[str, Any]) -> None:
        super().__init__(
            status_code=404,
            detail=f'Не найдена сущность "{entity_name}" по фильтру {filter}'
        )


class AlreadyExistsError(HTTPException):
    def __init__(self, entity_name: str, filter: dict[str, Any]) -> None:
        super().__init__(
            status_code=403,
            detail=f'Сущность "{entity_name}" с {filter}уже существует'
        )
