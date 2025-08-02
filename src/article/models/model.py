from base.model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from article.schemas.schema import ArticleSchema, ArticleSimpleSchema
from comment.models.model import CommentModel


class ArticleModel(BaseModel):
    __tablename__ = 'article'
    title: Mapped[str] = mapped_column()
    text: Mapped[str] = mapped_column()

    comments: Mapped[list['CommentModel']] = relationship(
        back_populates='article',
        lazy='selectin',
        uselist=True
    )

    @classmethod
    def from_schema(
        cls,
        schema: ArticleSimpleSchema | ArticleSchema
    ) -> 'ArticleModel':
        '''
        Конвертирует Pydantic-схему в SQLAlchemy-модель

        Args:
            schema (ArticleSimpleSchema | ArticleSchema): Pydantic-схема

        Returns:
            ArticleModel: SQLAlchemy-модель
        '''
        if type(schema) is ArticleSchema:
            return cls(
                id=schema.id,
                title=schema.title,
                text=schema.text
            )
        else:
            return cls(
                title=schema.title,
                text=schema.text
            )
