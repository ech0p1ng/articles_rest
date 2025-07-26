from pydantic import BaseModel, Field, ConfigDict


class BaseSimpleSchema(BaseModel):
    '''
    Базовая Pydantic-схема для сущностей без ID
    '''

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )


class BaseSchema(BaseSimpleSchema):
    '''
    Базовая Pydantic-схема для сущностей с ID

    Args:
        id (int): ID
    '''

    id: int = Field(gt=0, description="ID")
