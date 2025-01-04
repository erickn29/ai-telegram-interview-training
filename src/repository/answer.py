from sqlalchemy.ext.asyncio import AsyncSession

from model.answer import Answer
from repository.base import BaseRepository


class AnswerRepository(BaseRepository):
    model = Answer

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)
