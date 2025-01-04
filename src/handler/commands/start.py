from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from core.cache import cache
from core.database import db_conn
from enums.enums import CommandEnum
from keyboard.starting_kb import get_starting_kb
from service.user import UserService


router = Router()


@router.message(Command(CommandEnum.start.value))
async def start(message: Message):
    if not await cache.get_user(f"user:{message.from_user.id}"):
        async with db_conn.session_factory() as session:
            user_service = UserService(session=session)
            await user_service.create(
                tg_id=message.from_user.id,
                tg_url=message.from_user.url,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                tg_username=message.from_user.username,
            )
    await message.answer(CommandEnum.get_commands(), reply_markup=get_starting_kb())
