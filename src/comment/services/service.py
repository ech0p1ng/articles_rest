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
            CommentModel,
            model_name='comment'
        )
        self.__article_service = article_service

    async def create(self, model: CommentModel) -> CommentModel:
        '''
        Создание комментария

        Args:
            model (CommentModel): SQLAlchemy-модель комментария

        Raises:
            NotNotFoundError: Статья не существует
            AlreadyExistsError: Комментарий с таким ID уже существует

        Returns:
            CommentModel: SQLAlchemy-модель созданного комментария
        '''
        comment_filter = {"id": model.id}

        article_filter = {"id": model.article_id}
        article_exists = await self.__article_service.exists(article_filter)

        if not article_exists:
            raise NotFoundError(
                self.__article_service.model_name,
                article_filter
            )

        exists = await self.exists(comment_filter)
        if exists:
            raise AlreadyExistsError(self.model_name, comment_filter)
        return await super().create(model)

    async def get_trending(self) -> CommentModel:
        '''
        Получение случайного комментария

        Raises:
            NotFoundError: Нет ни одного комментария

        Returns:
            CommentModel: SQLAlchemy-модель комментария
        '''
        models = await self.get_all()
        if not models:
            raise NotFoundError(self.model_name)
        return random.choice(models)
