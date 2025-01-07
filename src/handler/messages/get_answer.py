import asyncio
import os

from pathlib import Path

from aiogram import F, Router
from aiogram.exceptions import AiogramError, TelegramBadRequest
from aiogram.types import Message

from bot import bot
from core.cache import cache
from keyboard.question_kb import get_question_kb
from model.error import create_error
from service.answer import AnswerServiceV1
from utils.speech_to_text import speech_to_text
from utils.text import normalize_to_markdown


router = Router()


@router.message(F.text)
async def get_text_answer(message: Message):
    key = f"tg_user_id:{message.from_user.id}:last_question"
    last_question_id = await cache.get(key)
    if not last_question_id:
        await message.answer("Вопрос не найден\. Выберите стек и начните тренировку\.")
        return
    processing = await message.answer("Обрабатываю ответ\.\.\.")
    answer_service = AnswerServiceV1()
    assessment = await answer_service.process_answer(
        int(last_question_id), message.from_user.id, message.text
    )
    if not assessment:
        await message.answer("Что-то пошло не так, попробуйте позже")
        return
    try:
        await processing.delete()
        await message.answer(assessment.text, reply_markup=get_question_kb())
    except (AiogramError, TelegramBadRequest) as e:
        await create_error(text=str(e))
        await message.answer("Что-то пошло не так, попробуйте позже")
        return


@router.message(F.voice)
async def get_voice_answer(message: Message):
    key = f"tg_user_id:{message.from_user.id}:last_question"
    last_question_id = await cache.get(key)
    if not last_question_id:
        await message.answer("Вопрос не найден\. Выберите стек и начните тренировку\.")
        return
    processing = await message.answer("Обрабатываю ответ\.\.\.")
    if message.voice.duration > 3 * 60:
        return await message.answer(
            "Аудио файл продолжительностью больше 3 минут не поддерживается"
        )
    folder = f"{Path(__file__).resolve().parent.parent.parent}/tmp/"
    file_name = f"{message.from_user.id}_{message.voice.file_unique_id}.ogg"
    check_tries = 10
    await bot.download(
        message.voice,
        destination=f"{folder}{file_name}",
    )
    while check_tries > 0:
        if os.path.exists(f"{folder}{file_name}"):
            break
        await asyncio.sleep(1)
        check_tries -= 1
    if not os.path.exists(f"{folder}{file_name}"):
        return await message.answer("Голосовое сообщение не найдено")
    text = await speech_to_text(f"{folder}{file_name}")
    os.remove(f"{folder}{file_name}")
    os.remove(f"{folder}{file_name.replace('.ogg', '.wav')}")
    answer_service = AnswerServiceV1()
    assessment = await answer_service.process_answer(
        int(last_question_id), message.from_user.id, text
    )
    if not assessment:
        await message.answer("Что-то пошло не так, попробуйте позже")
        return
    try:
        await processing.delete()
        await message.answer(normalize_to_markdown(f"Вот, что я распознал:\n'{text}'"))
        await message.answer(assessment.text, reply_markup=get_question_kb())
    except (AiogramError, TelegramBadRequest) as e:
        await create_error(text=str(e))
        await message.answer("Что-то пошло не так, попробуйте позже")
        return
