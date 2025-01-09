from datetime import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from core.database import db_conn
from enums.enums import CommandEnum
from repository.answer import AnswerRepository
from repository.user import UserRepository
from service.user import UserService


router = Router()


@router.message(Command(CommandEnum.stats.value))
async def stats(message: Message):
    async with db_conn.session_factory() as session:
        user_service = UserService(session=session)
        user = await user_service.find(tg_id=message.from_user.id)

    if not user or not user.is_admin:
        return await message.answer("Вы не админ")

    async with db_conn.session_factory() as session:
        user_repo = UserRepository(session=session)
        answers_repo = AnswerRepository(session=session)
        users_count = await user_repo.count(is_active=True)
        new_users_count = await user_repo.count(
            created_at={"gte": datetime.now().replace(hour=0, minute=0, second=0)}
        )
        answers_count = await answers_repo.count()
        answers_today = await answers_repo.filter(
            created_at={"gte": datetime.now().replace(hour=0, minute=0, second=0)}
        )
        active_users_today_count = set([a.user_id for a in answers_today])

    return await message.answer(
        f"Пользователи:\n"
        f"Всего: {users_count}\n"
        f"Новых за сегодня: {new_users_count}\n"
        f"\n"
        f"Ответов:\n"
        f"Всего: {answers_count}\n"
        f"Сегодня: {len(answers_today)}\n"
        f"\n"
        f"Активные пользователи сегодня:\n"
        f"{len(active_users_today_count)}\n"
    )
