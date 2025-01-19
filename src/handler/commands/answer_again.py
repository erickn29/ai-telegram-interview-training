from aiogram import F, Router
from aiogram.exceptions import AiogramError
from aiogram.types import Message

from enums.enums import CommandEnum
from keyboard.question_kb import get_question_kb
from model.error import create_error
from service.question import QuestionServiceV1
from utils.text import normalize_to_markdown


router = Router()


@router.message(F.text == CommandEnum.answer_again.value)
async def send_question_training(message: Message):
    question_service = QuestionServiceV1()
    question = await question_service.get_last_question_from_cache(message.from_user.id)
    if not question:
        return await message.answer("Вы еще не получили вопрос")
    try:
        await message.answer(
            normalize_to_markdown(question.text), reply_markup=get_question_kb()
        )
    except AiogramError as e:
        await create_error(text=str(e))
        await message.answer("Что\-то пошло не так, попробуйте ")
        return
