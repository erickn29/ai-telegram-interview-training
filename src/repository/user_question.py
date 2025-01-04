from sqlalchemy.ext.asyncio import AsyncSession

from model.user_question import UserQuestion
from repository.base import BaseRepository


class UserQuestionRepository(BaseRepository):
    model = UserQuestion

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)
