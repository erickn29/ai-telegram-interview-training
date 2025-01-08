from aiogram import F, Router
from aiogram.types import Message

from enums.enums import CommandEnum
from keyboard.starting_kb import get_starting_kb
from service.user import UserServiceV1
from utils.text import normalize_to_markdown


router = Router()


@router.message(F.text == CommandEnum.me.value)
async def me(message: Message):
    user_service = UserServiceV1()
    user_data = await user_service.get_user_data(message.from_user.id)
    answer = user_data or "Не удалось получить данные пользователя"
    await message.answer(normalize_to_markdown(answer), reply_markup=get_starting_kb())
