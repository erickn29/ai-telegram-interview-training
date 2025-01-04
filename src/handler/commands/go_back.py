from aiogram import F, Router
from aiogram.types import Message

from enums.enums import CommandEnum
from keyboard.starting_kb import get_starting_kb


router = Router()


@router.message(F.text == CommandEnum.go_back.value)
async def start(message: Message):
    await message.answer(CommandEnum.get_commands(), reply_markup=get_starting_kb())
