from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from article.services.service import ArticleService
from comment.services.service import CommentService
from storage.redis import RedisService
import redis.asyncio as redis

__redis_service_instance = RedisService()


async def redis_service() -> AsyncGenerator[redis.Redis, None]:
    '''
    Redis-сервис

    Yields:
        Iterator[AsyncGenerator[redis.Redis, None]]: Клиент Redis-сервиса
    '''
    async with __redis_service_instance.client() as client:
        yield client


def article_service(
    db: AsyncSession = Depends(get_db),
    service: redis.Redis = Depends(redis_service)
) -> ArticleService:
    '''
    Сервис статей

    Args:
        db (AsyncSession, optional): Асинхронная сессия БД. \
            Defaults to Depends(get_db).
        service (redis.Redis, optional): Redis-сервис. \
            Defaults to Depends(redis_service).

    Returns:
        ArticleService: _description_
    '''
    return ArticleService(db, service)


def comment_service(
    db: AsyncSession = Depends(get_db),
    article_service: ArticleService = Depends(article_service)
) -> CommentService:
    '''
    Сервис комментариев

    Args:
        db (AsyncSession, optional): Асинхронная сессия БД. \
            Defaults to Depends(get_db).
        article_service (ArticleService, optional): Сервис статей. \
            Defaults to Depends(article_service).

    Returns:
        CommentService: _description_
    '''
    return CommentService(db, article_service)
