from aiogram import F, Router
from aiogram.exceptions import AiogramError
from aiogram.types import Message

from core.cache import cache
from keyboard.question_kb import get_question_kb
from model.error import create_error
from service.answer import AnswerServiceV1


router = Router()


@router.message(F.text)
async def get_answer(message: Message):
    key = f"tg_user_id:{message.from_user.id}:last_question"
    last_question_id = await cache.get(key)
    if not last_question_id:
        await message.answer("Вопрос не найден\. Выберите стек и начните тренировку\.")
        return
    answer_service = AnswerServiceV1()
    assessment = await answer_service.process_answer(
        int(last_question_id), message.from_user.id, message.text
    )
    if not assessment:
        await message.answer("Что-то пошло не так, попробуйте позже")
        return
    try:
        await message.answer(assessment.text, reply_markup=get_question_kb())
    except AiogramError as e:
        await create_error(text=str(e))
        await message.answer("Что-то пошло не так, попробуйте позже")
        return
