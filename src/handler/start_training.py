from aiogram import F, Router, types
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from enums.enums import CommandEnum, StackEnum
from keyboard.select_stack_kb import get_select_stack_kb


router = Router()


@router.message(F.text == CommandEnum.start_training.value)
async def start_training(message: Message):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text=StackEnum.sql.value, callback_data=StackEnum.sql.value
        ),
        types.InlineKeyboardButton(
            text=StackEnum.git.value, callback_data=StackEnum.git.value
        ),
        types.InlineKeyboardButton(
            text=StackEnum.linux.value, callback_data=StackEnum.linux.value
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=StackEnum.network.value, callback_data=StackEnum.network.name
        ),
        types.InlineKeyboardButton(
            text=StackEnum.algorithm.value, callback_data=StackEnum.algorithm.name
        ),
        types.InlineKeyboardButton(
            text=StackEnum.computer_science.value,
            callback_data=StackEnum.computer_science.name,
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=StackEnum.python.value, callback_data=StackEnum.python.value
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text=StackEnum.django.value, callback_data=StackEnum.django.value
        ),
        types.InlineKeyboardButton(
            text=StackEnum.fastapi.value, callback_data=StackEnum.fastapi.value
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=StackEnum.javascript.value, callback_data=StackEnum.javascript.value
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text=StackEnum.react.value, callback_data=StackEnum.react.value
        ),
        types.InlineKeyboardButton(
            text=StackEnum.vue.value, callback_data=StackEnum.vue.value
        ),
        types.InlineKeyboardButton(
            text=StackEnum.angular.value, callback_data=StackEnum.angular.value
        ),
    )
    await message.answer(
        "Выберите стек для тренировки\n", reply_markup=builder.as_markup()
    )
    await message.answer(
        "Нажмите 'Готово' или вернитесь к выбору действия",
        reply_markup=get_select_stack_kb(),
    )
