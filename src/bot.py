from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from core.config import config


bot = Bot(
    token=config.bot.token,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2),
)
