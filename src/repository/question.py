from sqlalchemy import Sequence, select
from sqlalchemy.ext.asyncio import AsyncSession

from model import QuestionTechnology, Technology, UserQuestion
from model.question import Question
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

    async def get_answers_stats(self, user_id: int) -> dict:
        """
        select t.name technology_name, avg(average)::numeric(3,1) average_score
        from (
            select q.id question_id, t.name, max(a.score) average from answer a
            join user u on a.user_id = 14
            join question q on a.question_id = q.id
            join question_technology qt on qt.question_id = q.id
            join technology t on t.id = qt.technology_id
            group by q.id, t.name
        ) t
        group by t.name
        """
        pass
