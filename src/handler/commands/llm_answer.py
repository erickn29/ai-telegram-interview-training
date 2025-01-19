from aiogram import F, Router
from aiogram.exceptions import AiogramError
from aiogram.types import Message

from enums.enums import CommandEnum
from keyboard.question_kb import get_question_kb
from model.error import create_error
from service.ai_assessment import AIAssessmentServiceV1
from service.question import QuestionServiceV1


router = Router()


@router.message(F.text == CommandEnum.llm_answer.value)
async def send_question_training(message: Message):
    question_service = QuestionServiceV1()
    question = await question_service.get_last_question_from_cache(message.from_user.id)
    if not question:
        return await message.answer("Вы еще не получили вопрос")
    try:
        processing = await message.answer("Секундочку\.\.\.")
        ai_assessment_service = AIAssessmentServiceV1(question)
        ai_help = await ai_assessment_service.get_ai_help()
        await processing.delete()
        return await message.answer(ai_help, reply_markup=get_question_kb())
    except AiogramError as e:
        await create_error(text=str(e))
        await message.answer("Что\-то пошло не так, попробуйте позже")
        return
