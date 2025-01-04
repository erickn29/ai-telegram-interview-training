import json

from core.cache import cache
from core.database import db_conn
from model import AIAssessment, Answer, Question, User
from repository.answer import AnswerRepository
from repository.question import QuestionRepository
from repository.user import UserRepository
from service.ai_assessment import AIAssessmentServiceV1


class AnswerServiceV1:

    def __init__(self):
        self.session = db_conn.session_factory()

    async def process_answer(
        self, question_id: int, user_id: int, text: str = ""
    ) -> AIAssessment | None:
        async with self.session.begin():
            answer_repo = AnswerRepository(session=self.session)
            user_repo = UserRepository(session=self.session)
            question_repo = QuestionRepository(session=self.session)

            user = await user_repo.find(tg_id=user_id)
            question = await question_repo.find(id=question_id)
            if not question or not user:
                return

            answer = await answer_repo.create(
                text=text, user_id=user.id, question_id=question.id, commit=False
            )
        technologies = await cache.get(f"tg_user_id:{user_id}:stack")
        assessment = await self._get_ai_assessment(
            question, answer, user, json.loads(technologies)
        )
        return assessment

    async def _get_ai_assessment(
        self, question: Question, answer: Answer, user: User, technologies: list[str]
    ) -> AIAssessment | None:
        if not any([question, answer, user, technologies]):
            return
        assessment_service = AIAssessmentServiceV1(
            question=question, answer=answer, user=user, technologies=technologies
        )
        response = await assessment_service.get_ai_assessment()
        if not response:
            return
        assessment, score = response
        if score <= 1:
            return assessment
        async with self.session.begin():
            answer_repo = AnswerRepository(session=self.session)
            await answer_repo.update(
                answer,
                score=score,
                commit=False,
            )
        return assessment
