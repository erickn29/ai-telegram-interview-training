from aiogram import F, Router
from aiogram.types import Message

from enums.enums import CommandEnum
from keyboard.question_kb import get_question_kb


router = Router()


@router.message(F.text == CommandEnum.run_training.value)
async def run_training(message: Message):
    await message.answer(
        (
            "Нажмите на кнопку 'Ешё вопрос' для начала тренировки\.\n"
            "Введите ответ на вопрос и отправьте мне сообщение\."
        ),
        reply_markup=get_question_kb(),
    )
