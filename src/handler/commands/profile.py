from aiogram import F, Router
from aiogram.types import Message

from enums.enums import CommandEnum


router = Router()


@router.message(F.text == CommandEnum.me.value)
async def me(message: Message):
    await message.answer("Это мой профиль")
