from pydantic import Field
from base.schema import BaseSchema, BaseSimpleSchema


class CommentSimpleSchema(BaseSimpleSchema):
    '''
    Упрощенная Pydantic-схема коментария

    Args:
        text (str): Содержимое коментария
        score (int): Оценка коментария от 0 до 5 включительно
        article_id (int): ID статьи, для которой написан этот коментарий
    '''
    text: str
    score: int = Field(ge=0, le=5)
    article_id: int = Field(ge=1)


class CommentSchema(CommentSimpleSchema, BaseSchema):
    '''
    Pydantic-схема коментария

    Args:
        id (int): ID
        text (str): Содержимое коментария
        score (int): Оценка коментария от 0 до 5 включительно
        article_id (int): ID статьи, для которой написан этот коментарий
    '''
    pass
