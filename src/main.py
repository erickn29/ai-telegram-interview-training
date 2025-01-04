import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from core.config import config
from handler.auth import router as auth_router
from handler.get_answer import router as get_answer_router
from handler.go_back import router as go_back_router
from handler.run_training import router as run_training_router
from handler.select_stack import router as select_stack_router
from handler.send_question import router as send_question_router
from handler.start import router as start_router
from handler.start_training import router as start_training_router


async def main():
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2),
    )
    dp = Dispatcher()
    dp.include_routers(
        send_question_router,
        start_router,
        go_back_router,
        start_training_router,
        select_stack_router,
        auth_router,
        run_training_router,
        get_answer_router,
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
