from sqlalchemy import RowMapping, Sequence, text
from sqlalchemy.ext.asyncio import AsyncSession

from model.user import User
from repository.base import BaseRepository


class UserRepository(BaseRepository):
    model = User

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)

    async def get_stats_by_technology(self, user_id: int) -> Sequence[RowMapping]:
        """
        Возвращает статистику юзера по технологиям
        """
        raw_result = await self.session.execute(
            text(
                """
                select t.name technology_name, count(question_id) user_answers, 
                sum(average)::int user_score, count(t.name) * 10 max_score
                from (
                    select q.id question_id, t.name, max(a.score) average from answer a
                    join user u on a.user_id = :user_id
                    join question q on a.question_id = q.id
                    join question_technology qt on qt.question_id = q.id
                    join technology t on t.id = qt.technology_id
                    group by q.id, t.name
                ) t
                group by t.name
                order by user_score
                limit 20
                """
            ),
            {"user_id": user_id},
        )
        result = raw_result.mappings().all()
        return result
