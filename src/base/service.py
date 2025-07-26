from typing import TypeVar, Any
from base.model import BaseModel
from base.repository import BaseRepository
from sqlalchemy.orm.strategy_options import _AttrType
from sqlalchemy import Select, delete, select
from sqlalchemy.orm import selectinload
from exceptions.exception import NotFoundError

M = TypeVar("M", bound=BaseModel)


class BaseService[M]:
    '''
    Базовый класс бизнес-логики сущности

    Generics:
        M: Класс SQLAlchemy-модели сущности
    '''

    _wrong_filter_error = ValueError(
        'Фильтр поиска должен включать в себя хотя бы одну пару '
        '{"Название_атрибута": Значение_атрибута}'
    )

    model_class: type[M]

    def __init__(
        self,
        repository: BaseRepository,
        model_class: type[M],
        model_name: str
    ) -> None:
        '''
        Базовый класс бизнес-логики сущности

        Args:
            repository (BaseRepository): Репозиторий для работы с БД
            model_class (type[M]): Класс SQLAlchemy-модели
            model_name (str): Название SQLAlchemy-модели на английском
        '''
        self.repository = repository
        self.model_class = model_class
        self.model_name = model_name

    async def create(self, model: M) -> M:
        return await self.repository.create(model)

    async def get(
        self,
        filter: dict[str, Any],
        model_attrs: list[_AttrType] = []
    ) -> M:
        '''
        Поиск в БД сущности по фильтру

        Args:
            filter (dict[str, Any]): Фильтр поиска сущности в БД. \
                `{"Название_атрибута": Значение_атрибута}`
            model_attrs (list[_AttrType]): Дополнительно подгружаемые сложные \
                аттрибуты SQLAlchemy модели

        '''

        if not self._is_correct_filter(filter):
            raise self._wrong_filter_error

        statement = self._add_model_attrs_to_statement(
            select(self.model_class),
            model_attrs
        )
        model = await self.repository.scalars_one_or_none(
            statement.filter_by(**filter)
        )
        if not model:
            raise NotFoundError(self.model_name, filter)
        await self.repository.db.flush()
        return model

    async def get_multiple(
        self,
        filter: dict[str, Any],
        model_attrs: list[_AttrType] = []
    ) -> list[M]:
        '''
        Поиск в БД нескольких сущностей по фильтру

        Args:
            filter (dict[str, Any]): Фильтр поиска сущности в БД. \
                `{"Название_атрибута": Значение_атрибута}`
            model_attrs (list[_AttrType]): Дополнительно подгружаемые сложные \
                аттрибуты SQLAlchemy модели
        '''
        statement = self._add_model_attrs_to_statement(
            select(self.model_class),
            model_attrs
        )
        models = await self.repository.scalars_all(
            statement.filter_by(**filter)
        )
        await self.repository.db.flush()
        return list(models)

    async def exists(
        self,
        filter: dict[str, Any],
        model_attrs: list[_AttrType] = []
    ) -> bool:
        '''
        Проверка на существование сущности по фильтру

        Args:
            filter (dict[str, Any]): Фильтр поиска сущности в БД. \
                `{"Название_атрибута": Значение_атрибута}`
        '''
        if not self._is_correct_filter(filter):
            raise self._wrong_filter_error

        statement = self._add_model_attrs_to_statement(
            select(self.model_class),
            model_attrs
        )
        model = await self.repository.scalars_one_or_none(
            statement.filter_by(**filter)
        )
        await self.repository.db.flush()
        return bool(model)

    async def get_all(
        self,
        model_attrs: list[_AttrType] = []
    ) -> list[M]:
        '''
        Поиск всех сущностей

        Args:
            model_attrs (list[_AttrType]): Дополнительно подгружаемые сложные \
                аттрибуты SQLAlchemy модели
        '''
        statement = self._add_model_attrs_to_statement(
            select(self.model_class),
            model_attrs
        )
        models = await self.repository.scalars_all(
            statement
        )
        await self.repository.db.flush()
        return list(models)

    async def update(self, model: M) -> M | None:
        '''
        Обновление сущности

        Args: 
            model (M): SQLAlchemy-модель сущности
        '''
        return await self.repository.update(model)

    async def delete(self, filter: dict[str, Any]) -> None:
        '''
        Удаление сущностей из БД по фильтру

        Args:
            filter (dict[str, Any]): Фильтр поиска сущности в БД. \
                `{"Название_атрибута": Значение_атрибута}`
        '''
        exists = await self.exists(filter)
        if not exists:
            raise NotFoundError(self.model_name, filter)
        statement = delete(self.model_class).filter_by(**filter)
        await self.repository.delete(statement)

    def _add_model_attrs_to_statement(
        self,
        statement: Select,
        model_attrs: list[_AttrType] = []
    ) -> Select:
        '''
        Добавление стейтменту связанных атрибутов SQLAlchemy-модели
        '''
        if model_attrs:
            options = [selectinload(attr) for attr in model_attrs]
            statement.options(*options)
        return statement

    def _is_correct_filter(
        self,
        filter: dict[str, Any],
        raise_exc=True
    ) -> bool:
        '''
        Проверка фильтра поиска

        Args:
            filter (dict[str, Any]): Проверяемый фильтр поиска
            raise_exc (bool): Вызывать ли исключения в случае некорректности \
                фильтра поиска (по-умолчанию - `True`)

        Returns:
            bool: `True` - фильтр корректный, иначе `False`
        '''

        if filter is None:
            if raise_exc:
                raise ValueError(
                    'Фильтр поиска должен включать в себя хотя бы одну пару '
                    '{"Название_атрибута": Значение_атрибута}'
                )
            return False
        return True
