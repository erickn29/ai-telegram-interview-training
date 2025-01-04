from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from enums.enums import CommandEnum


def get_select_stack_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=CommandEnum.go_back.value)
    kb.button(text=CommandEnum.run_training.value)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
