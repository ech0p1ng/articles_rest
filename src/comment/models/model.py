from base.model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from comment.schemas.schema import CommentSchema, CommentSimpleSchema
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from article.models.model import ArticleModel


class CommentModel(BaseModel):
    __tablename__ = 'comment'
    score: Mapped[int] = mapped_column()
    text: Mapped[str] = mapped_column()

    article_id: Mapped[int] = mapped_column(ForeignKey('article.id'))
    article: Mapped['ArticleModel'] = relationship(
        back_populates='comments',
        lazy='selectin'
    )

    @classmethod
    def from_schema(
        cls,
        schema: CommentSimpleSchema | CommentSchema
    ) -> 'CommentModel':
        '''
        Конвертирует Pydantic-схему в SQLAlchemy-модель

        Args:
            schema (CommentSimpleSchema | CommentSchema): Pydantic-схема

        Returns:
            CommentModel: SQLAlchemy-модель
        '''
        if type(schema) is CommentSchema:
            return cls(
                id=schema.id,
                text=schema.text,
                score=schema.score,
                article_id=schema.article_id
            )
        else:
            return cls(
                text=schema.text,
                score=schema.score,
                article_id=schema.article_id
            )
