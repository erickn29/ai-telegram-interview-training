from collections.abc import Sequence
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from model.base import Base, ModelObject
from repository.base import BaseRepository


class BaseService:
    def __init__(self, session: AsyncSession, repository: type[BaseRepository]):
        self.session = session
        self.repository = repository(session=session)

    async def create(self, **model_data) -> ModelObject:
        return await self.repository.create(**model_data)

    async def get(self, **filters) -> ModelObject | None:
        return await self.repository.get(**filters)

    async def delete(self, instance: Base) -> None:
        return await self.repository.delete(instance)

    async def update(self, instance: Base, **model_data) -> ModelObject:
        return await self.repository.update(instance, **model_data)

    async def all(
        self, order_by: list[InstrumentedAttribute] | None = None
    ) -> Sequence[ModelObject]:
        return await self.repository.all(order_by)

    async def filter(
        self,
        filters: dict[str, Any],
        exclude_data: dict[InstrumentedAttribute, Any] | None = None,
        order_by: list[InstrumentedAttribute] | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Sequence[ModelObject]:
        return await self.repository.filter(
            filters=filters,
            order_by=order_by,
            exclude_data=exclude_data,
            limit=limit,
            offset=offset,
        )

    async def get_or_create(
        self, filters: dict[str, Any], **model_data
    ) -> tuple[ModelObject, bool]:
        return await self.repository.get_or_create(filters, **model_data)

    async def update_or_create(
        self, filters: dict[str, Any], **model_data
    ) -> tuple[ModelObject, bool]:
        return await self.repository.update_or_create(filters, **model_data)

    async def exists(
        self,
        filters: dict[str, Any],
        exclude_data: dict[InstrumentedAttribute, Any] | None = None,
    ) -> bool:
        return await self.repository.exists(filters, exclude_data)

    async def count(
        self,
        filters: dict[str, Any],
        exclude_data: dict[InstrumentedAttribute, Any] | None = None,
    ) -> int:
        return await self.repository.count(filters, exclude_data)
