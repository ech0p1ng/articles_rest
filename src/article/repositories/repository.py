from sqlalchemy.ext.asyncio import AsyncSession
from base.repository import BaseRepository
from article.models.model import ArticleModel


class ArticleRepository(BaseRepository[ArticleModel]):
    '''
    Класс обработки бизнес-логики статей
    '''

    def __init__(self, db: AsyncSession) -> None:
        '''
        Класс обработки бизнес-логики статей

        Args:
            db (AsyncSession): Асинхронная сессия БД
        '''
        super().__init__(db)
