from base.schema import BaseSchema, BaseSimpleSchema
from comment.schemas.schema import CommentSchema


class ArticleSimpleSchema(BaseSimpleSchema):
    '''
    Упрощенная Pydantic-схема статьи

    Args:
        title (str): Название статьи
        text (str): Содержимое статьи
    '''
    title: str
    text: str


class ArticleSchema(ArticleSimpleSchema, BaseSchema):
    '''
    Pydantic-схема статьи

    Args:
        id (int): ID
        title (str): Название статьи
        text (str): Содержимое статьи
        comments (list[CommentSchema]): Коментарии статьи
    '''
    comments: list[CommentSchema]
    pass
