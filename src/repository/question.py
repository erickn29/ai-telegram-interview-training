from sqlalchemy import Sequence, select
from sqlalchemy.ext.asyncio import AsyncSession

from model import Question, QuestionTechnology, Technology, UserQuestion
from repository.base import BaseRepository


class QuestionRepository(BaseRepository):
    model = Question

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)

    async def get_questions(self, technologies: list[str]) -> Sequence[Question]:
        sub_query_technologies = select(Technology.id).where(
            Technology.name.in_(technologies)
        )
        query = (
            select(self.model)
            .join(QuestionTechnology, QuestionTechnology.question_id == self.model.id)
            .where(
                QuestionTechnology.technology_id.in_(sub_query_technologies),
            )
            .distinct(self.model.id, self.model.created_at)
            .order_by(self.model.created_at)
        )
        result = await self.session.scalars(query)
        return result.all()

    async def get_unanswered_questions(
        self, user_id: int, technologies: list[str]
    ) -> Sequence[Question]:
        sub_query_technologies = select(Technology.id).where(
            Technology.name.in_(technologies)
        )
        sub_query_user_questions = select(UserQuestion.question_id).where(
            UserQuestion.user_id == user_id
        )
        query = (
            select(self.model)
            .join(QuestionTechnology)
            .where(
                QuestionTechnology.technology_id.in_(sub_query_technologies),
                QuestionTechnology.question_id == self.model.id,
                self.model.id.not_in(sub_query_user_questions),
                self.model.published == True,
            )
            .distinct(self.model.id, self.model.created_at)
            .order_by(self.model.created_at)
        )
        result = await self.session.scalars(query)
        questions = result.all()
        return questions
