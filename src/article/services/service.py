from base.service import BaseService
from article.models.model import ArticleModel
from article.repositories.repository import ArticleRepository
from sqlalchemy.ext.asyncio import AsyncSession
from exceptions.exception import AlreadyExistsError, NotFoundError
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
            ArticleModel,
            model_name='Статья'
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
            raise AlreadyExistsError(self.model_name, filter)
        return await super().create(model)

    async def get_tranding(self) -> ArticleModel:
        '''
        Получение случайной статьи
        '''
        models = await self.get_all()
        if not models:
            raise NotFoundError(self.model_name)
        return random.choice(models)
