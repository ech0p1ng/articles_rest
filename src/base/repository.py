from typing import TypeVar, Sequence
from sqlalchemy import ScalarResult, Select, Delete
from sqlalchemy.ext.asyncio import AsyncSession
from base.model import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository[T: BaseModel]:
    '''
    Базовый класс обработки данных из БД

    Attibutes:
        T (Any): Класс SQLAlchemy-модели сущности

    Args:
        db (AsynSession): Асинхронная сессия БД

    '''

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        pass

    async def scalars_all(self, statement: Select[tuple[T]]) -> Sequence[T]:
        return (await self.db.execute(statement)).scalars().all()

    async def scalars_one(self, statement: Select[tuple[T]]) -> T:
        return (await self.db.execute(statement)).scalars().one()

    async def scalars_one_or_none(
        self,
        statement: Select[tuple[T]]
    ) -> T | None:
        return (await self.db.execute(statement)).scalars().one_or_none()

    async def scalars_unique(
        self,
        statement: Select[tuple[T]]
    ) -> ScalarResult[T] | None:
        return (await self.db.execute(statement)).scalars().unique()

    async def create(self, model: T) -> T:
        '''
        Добавление сущности в БД

        Args:
            model (T): SQLAlchemy-модель сущности

        Returns:
            T: Сущность, с обновленными данными из БД
        '''
        self.db.add(model)
        await self.db.flush()
        await self.db.refresh(model)
        return model

    async def update(
        self,
        model: T,
    ) -> T | None:
        '''
        Обновление сущности

        Args:
            model (T): SQLAlchemy-модель сущности с обновленными данными

        Returns:
            T: Обновленная SQLAlchemy-модель сущности из БД

        Raises:
            ValueError: Неверный фильтр поиска
        '''

        merged = await self.db.merge(model)
        await self.db.flush()
        await self.db.refresh(merged)
        return merged

    async def delete(self, statement: Delete) -> None:
        '''
        Удаление сущности из БД

        Args:
            statement (Delete): Стейтмент для удаления сущностей из БД
        '''
        await self.db.execute(statement)
        await self.db.flush()
