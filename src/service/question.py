import json
import random

from core.cache import cache
from core.database import db_conn
from model import Question, User
from repository.question import QuestionRepository
from repository.user import UserRepository
from repository.user_question import UserQuestionRepository


class QuestionServiceV1:

    @staticmethod
    async def _get_user_stack(user_tg_id: int) -> list[str] | None:
        if not user_tg_id:
            return None
        key = f"tg_user_id:{user_tg_id}:stack"
        user_stack = await cache.get(key)
        if not user_stack:
            return None
        return json.loads(user_stack)

    async def get_question_for_training(self, user_tg_id: int) -> Question | None:
        stack_list = await self._get_user_stack(user_tg_id) or ["python"]
        session = db_conn.session_factory()

        async with session.begin():
            user_repo = UserRepository(session=session)
            question_repo = QuestionRepository(session=session)

            user = await user_repo.find(tg_id=user_tg_id)
            if not user:
                return None

            questions = await question_repo.get_unanswered_questions(
                user_id=user.id, technologies=stack_list
            )
            if not questions:
                questions = await question_repo.get_questions(technologies=stack_list)

        question = random.choice(questions) if questions else None
        if question:
            await self._save_user_question(user, question)
            await self._add_last_question_to_cache(user_tg_id, question.id)
        return question

    @staticmethod
    async def _save_user_question(user: User, question: Question):
        if not user or not question:
            return

        session = db_conn.session_factory()
        async with session.begin():
            user_question_repo = UserQuestionRepository(session=session)
            await user_question_repo.get_or_create(
                filters=[
                    "user_id",
                    "question_id",
                ],
                user_id=user.id,
                question_id=question.id,
                commit=False,
            )

    @staticmethod
    async def _add_last_question_to_cache(user_tg_id: int, question_id: int):
        if not user_tg_id or not question_id:
            return
        key = f"tg_user_id:{user_tg_id}:last_question"
        ttl = 60 * 60 * 24 * 7 * 55
        await cache.set(key, question_id, ttl)

    @staticmethod
    async def get_last_question_from_cache(user_tg_id: int) -> Question | None:
        key = f"tg_user_id:{user_tg_id}:last_question"
        last_question_id = await cache.get(key)
        if not last_question_id:
            return None
        session = db_conn.session_factory()
        async with session.begin():
            question_repo = QuestionRepository(session=session)
            question = await question_repo.find(id=int(last_question_id))
            return question
