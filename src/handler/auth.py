import uuid

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

from core.cache import cache
from core.config import config
from core.database import db_conn
from enums.enums import CommandEnum
from service.user import UserService


router = Router()


@router.message(Command(CommandEnum.auth.value))
async def auth(message: Message):
    async with db_conn.session_factory() as session:
        user_service = UserService(session=session)
        user = await user_service.find(tg_id=message.from_user.id)

    if not user or not user.is_admin:
        return await message.answer("Вы не админ")

    temp_key = uuid.uuid4().hex
    await cache.set(temp_key, str(user.id), config.auth.ttl)

    url = f"{config.auth.host}:{config.auth.port}/admin?token={temp_key}"
    return await message.answer(f'<a href="{url}">{url}</a>', parse_mode=ParseMode.HTML)
