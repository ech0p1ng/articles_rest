from base.service import BaseService
from comment.models.model import CommentModel
from comment.repositories.repository import CommentRepository
from sqlalchemy.ext.asyncio import AsyncSession
from exceptions.exception import AlreadyExistsError
from article.services.service import ArticleService
from exceptions.exception import NotFoundError
import random


class CommentService(BaseService[CommentModel]):
    '''
    Бизнес-логика для коментариев
    '''

    def __init__(
        self,
        db: AsyncSession,
        article_service: ArticleService
    ) -> None:
        '''
        Бизнес-логика для коментариев

        Args:
            db (AsyncSession): Асинхронная сессия БД
            article_service (ArticleService): Бизнес-логика статей
        '''
        super().__init__(
            CommentRepository(db),
            CommentModel
        )
        self.__article_service = article_service

    async def create(self, model: CommentModel) -> CommentModel:
        '''
        Создание коментария

        Args:
            model (CommentModel): SQLAlchemy-модель коментария

        Raises:
            NotFoundError: Коментарий или статья не найдены
        '''
        comment_filter = {"id": model.id}

        article_filter = {"id": model.article_id}
        article_exists = await self.__article_service.exists(article_filter)

        if not article_exists:
            raise NotFoundError('Статья', article_filter)

        exists = await self.exists(comment_filter)
        if exists:
            raise AlreadyExistsError('Коментарий', comment_filter)
        return await super().create(model)

    async def get_trending(self) -> CommentModel:
        '''
        Получение случайного коментария
        '''
        return random.choice(await self.get_all())
