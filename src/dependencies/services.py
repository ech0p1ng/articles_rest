from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from article.services.service import ArticleService
from comment.services.service import CommentService
from storage.redis import RedisService
import redis.asyncio as redis

__redis_service_instance = RedisService()


def article_service(
    db: AsyncSession = Depends(get_db)
) -> ArticleService:
    return ArticleService(db)


def comment_service(
    db: AsyncSession = Depends(get_db),
    article_service: ArticleService = Depends(article_service)
) -> CommentService:
    return CommentService(db, article_service)


def redis_service(
    client: redis.Redis = Depends(__redis_service_instance.client)
) -> redis.Redis:
    return client
