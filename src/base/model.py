from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from sqlalchemy.orm import Mapped, mapped_column


class BaseModel(DeclarativeBase):
    '''
    Базовая SQLAlchemy-модель сущности из БД

    Args:
        id (int): ID сущности в БД
    '''
    metadata = MetaData()

    model_config = {
        'from_attributes': True
    }

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.id == value.id
        return NotImplemented
