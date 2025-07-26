from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from article.services.service import ArticleService
from comment.services.service import CommentService


def article_service(
    db: AsyncSession = Depends(get_db)
) -> ArticleService:
    return ArticleService(db)


def comment_service(
    db: AsyncSession = Depends(get_db)
) -> CommentService:
    return CommentService(db)
