from base.service import BaseService
from article.models.model import ArticleModel
from article.repositories.repository import ArticleRepository
from sqlalchemy.ext.asyncio import AsyncSession
from exceptions.exception import AlreadyExistsError
import random


class ArticleService(BaseService[ArticleModel]):
    '''
    Бизнес-логика для статей
    '''

    def __init__(
        self,
        db: AsyncSession
    ) -> None:
        '''
        Бизнес-логика для статей

        Args:
            db (AsyncSession): Асинхронная сессия БД
        '''
        super().__init__(
            ArticleRepository(db),
            ArticleModel
        )

    async def create(self, model: ArticleModel) -> ArticleModel:
        '''
        Создание статьи

        Args:
            model (ArticleModel): SQLAlchemy-модель статьи
        '''
        filter = {"id": model.id}
        exists = await self.exists(filter)
        if exists:
            raise AlreadyExistsError('Статья', filter)
        return await super().create(model)

    async def get_tranding(self) -> ArticleModel:
        '''
        Получение случайной статьи
        '''
        return random.choice(await self.get_all())
