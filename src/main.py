import asyncio
import logging
import sys

from aiogram import Dispatcher

from bot import bot
from handler.callbacks.select_stack import router as select_stack_router
from handler.commands.auth import router as auth_router
from handler.commands.go_back import router as go_back_router
from handler.commands.profile import router as profile_router
from handler.commands.run_training import router as run_training_router
from handler.commands.send_question import router as send_question_router
from handler.commands.start import router as start_router
from handler.commands.start_training import router as start_training_router
from handler.messages.get_answer import router as get_answer_router


async def main():
    dp = Dispatcher()
    dp.include_routers(
        send_question_router,
        start_router,
        go_back_router,
        start_training_router,
        select_stack_router,
        auth_router,
        run_training_router,
        profile_router,
        get_answer_router,
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
