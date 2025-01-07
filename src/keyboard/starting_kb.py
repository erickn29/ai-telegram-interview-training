from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from enums.enums import CommandEnum


def get_starting_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    # kb.button(text=CommandEnum.start_interview.value)
    kb.button(text=CommandEnum.start_training.value)
    kb.button(text=CommandEnum.me.value)
    kb.button(text=CommandEnum.leaders.value)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
