from sqlalchemy.ext.asyncio import AsyncSession

from model.user import User
from repository.base import BaseRepository


class UserRepository(BaseRepository):
    model = User

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)
