from sqlalchemy.ext.asyncio import AsyncSession

from model.technology import Technology
from repository.base import BaseRepository


class TechnologyRepository(BaseRepository):
    model = Technology

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)
