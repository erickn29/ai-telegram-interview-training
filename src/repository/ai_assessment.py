from sqlalchemy.ext.asyncio import AsyncSession

from model.ai_assessment import AIAssessment
from repository.base import BaseRepository


class AIAssessmentRepository(BaseRepository):
    model = AIAssessment

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)
