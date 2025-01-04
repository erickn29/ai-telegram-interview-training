import json

from aiogram import F, Router, types

from core.cache import cache
from enums.enums import StackEnum


router = Router()


@router.callback_query(F.data)
async def handle_stack_callback(callback: types.CallbackQuery):
    stacks = StackEnum.get_stacks()
    key = f"tg_user_id:{callback.from_user.id}:stack"
    ttl = 60 * 60 * 24 * 7 * 55
    if callback.data in stacks:
        if user_stack := await cache.get(key):
            user_stack: list[str] = json.loads(user_stack)
            if callback.data in user_stack:
                user_stack.remove(callback.data)
                await cache.set(key, json.dumps(user_stack), ttl)
                return await callback.answer(text=f"Вы удалили '{callback.data}'")
            user_stack.append(callback.data)
            await cache.set(key, json.dumps(user_stack), ttl)
            return await callback.answer(text=f"Вы добавили '{callback.data}'")
        await cache.set(key, json.dumps([callback.data]), ttl)
        return await callback.answer(text=f"Вы добавили '{callback.data}'")
    return await callback.answer(text="Непредвиденная ошибка")
