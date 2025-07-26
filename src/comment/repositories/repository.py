from sqlalchemy.ext.asyncio import AsyncSession
from base.repository import BaseRepository
from comment.models.model import CommentModel


class CommentRepository(BaseRepository[CommentModel]):
    '''
    Класс обработки бизнес-логики коментариев
    '''

    def __init__(self, db: AsyncSession) -> None:
        '''
        Класс обработки бизнес-логики коментариев

        Args:
            db (AsyncSession): Асинхронная сессия БД
        '''
        super().__init__(db)
