import uuid

from datetime import datetime
from typing import Annotated, TypeVar

from sqlalchemy import TIMESTAMP, UUID, BigInteger, MetaData, inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from core.config import config


TIMESTAMP_WITH_TIMEZONE = TIMESTAMP(timezone=True)


uuid_pk = Annotated[
    uuid.UUID,
    mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True
    ),
]
int_pk = Annotated[
    int,
    mapped_column(BigInteger, primary_key=True, autoincrement=True, unique=True),
]
created_at = Annotated[
    datetime,
    mapped_column(
        TIMESTAMP_WITH_TIMEZONE,
        default=datetime.now,
        nullable=False,
        doc="Дата создания",
    ),
]
updated_at = Annotated[
    datetime,
    mapped_column(
        TIMESTAMP_WITH_TIMEZONE,
        default=datetime.now,
        nullable=False,
        onupdate=datetime.now,
        doc="Дата изменения",
    ),
]


class Base(DeclarativeBase):
    verbose_name: str = "Базовая модель"

    id: Mapped[int_pk]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    metadata = MetaData(naming_convention=config.db.naming_convention)

    @classmethod
    def ordering(cls):
        return [cls.created_at]

    @property
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self) -> str:
        return f"<{self.id} | {self.verbose_name}>"


Model = TypeVar("Model", bound=type[Base])
ModelObject = TypeVar("ModelObject", bound=Base)
