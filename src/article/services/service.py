from base.service import BaseService
from article.models.model import ArticleModel
from article.repositories.repository import ArticleRepository
from sqlalchemy.ext.asyncio import AsyncSession
from exceptions.exception import AlreadyExistsError, NotFoundError
import random
from redis.asyncio import Redis
from article.schemas.schema import ArticleSchema


class ArticleService(BaseService[ArticleModel]):
    '''
    Бизнес-логика для статей
    '''

    def __init__(
        self,
        db: AsyncSession,
        redis_service: Redis
    ) -> None:
        '''
        Бизнес-логика для статей

        Args:
            db (AsyncSession): Асинхронная сессия БД
        '''
        super().__init__(
            ArticleRepository(db),
            ArticleModel,
            model_name='article'
        )
        self.redis_service = redis_service

    async def create(self, model: ArticleModel) -> ArticleModel:
        '''
        Создание статьи

        Args:
            model (ArticleModel): SQLAlchemy-модель статьи
        '''
        filter = {"id": model.id}
        exists = await self.exists(filter)
        if exists:
            raise AlreadyExistsError(self.model_name, filter)
        return await super().create(model)

    async def get_tranding(self) -> ArticleModel:
        '''
        Получение случайной статьи

        Returns:
            ArticleModel: SQLAlchemy-модель случайной статьи
        '''
        models = await self.get_all()
        if not models:
            raise NotFoundError(self.model_name)
        return random.choice(models)

    async def get_cached(self, id: int) -> ArticleModel:
        '''
        Получение кешированной статьи из Redis

        Args:
            id (int): ID статьи`

        Returns:
            ArticleModel: SQLAlchemy-модель найденой статьи
        '''

        try:
            model = await self.__get_from_cache(id)
        except NotFoundError:
            print(f'Cached {self.model_name} not found')
            filter = {'id': id}
            model = await self.get(filter)
            await self.__cache(model, expire_time_seconds=30)
        return model

    async def __get_from_cache(self, id: int) -> ArticleModel:
        '''
        Получает из Redis кэшированные данные о SQLAlchemy-модели

        Args:
            id (int): ID SQLAlchemy-модели

        Returns:
            ArticleModel: SQLAlchemy-модель

        Raises:
            NotFoundError: Не удалось найти
        '''
        raw = await self.redis_service.get(self.__get_key(id))
        if raw:
            schema = ArticleSchema.model_validate_json(raw)
            model = ArticleModel.from_schema(schema)
            return model
        raise NotFoundError(self.model_name, {'id': id})

    async def __delete_from_cache(self, id: int) -> None:
        '''
        Удаление из Redis кэшированных данных

        Args:
            id (int): ID SQLAlchemy-модели

        Raises:
            NotFoundError: Не удалось найти
        '''
        await self.redis_service.delete(self.__get_key(id))

    async def __cache(
        self,
        model: ArticleModel,
        expire_time_seconds: int = 0
    ) -> None:
        '''
        Кеширует данные о SQLAlchemy-модели в Redis

        Args:
            model (ArticleModel): SQLAlchemy-модель
            expire_time_seconds (int): Время жизни кэша в Redis. \
                Если `expire_time_seconds <= 0`, то время жизни бесконечно
        '''
        key = self.__get_key(model.id)
        schema = ArticleSchema.model_validate(model)
        json_data = schema.model_dump_json()
        if expire_time_seconds > 0:
            await self.redis_service.set(
                key,
                json_data,
                ex=expire_time_seconds
            )
        else:
            await self.redis_service.set(key, json_data)

    def __get_key(self, id: int) -> str:
        '''
        Получение ключа значения для Redis

        Args:
            id (int): ID SQLAlchemy-модели

        Returns:
            str: Ключ вида `название_модели:id`
        '''
        return f'{self.model_name}:{id}'
