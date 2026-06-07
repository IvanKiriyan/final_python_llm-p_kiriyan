from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from app.core.jwt import decode_and_validate
from app.infra.redis import get_redis
from app.tasks.llm_tasks import llm_request

router = Router()

def token_key(user_id: int) -> str:
    return f"token:{user_id}"

@router.message(Command("token"))
async def cmd_token(message: Message) -> None:
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Использование: /token <jwt>")
        return
    
    token = parts[1].strip()
    try:
        decode_and_validate(token)
    except ValueError as e:
        await message.answer(f"Некорректный токен: {e}")
        return
    
    redis = await get_redis()
    await redis.set(token_key(message.from_user.id), token)
    await message.answer("Успешно, токен сохранен. Задавайте свои вопросы")

@router.message()
async def cmd_text(message: Message) -> None:
    redis = await get_redis()
    token = await redis.get(token_key(message.from_user.id))

    if not token:
        await message.answer(
            "Отсутствует токен. " \
            "Получите его в Auth Service и отправьте командой /token <jwt>"
        )
        return
    
    try:
        decode_and_validate(token)
    except ValueError:
        await message.answer(
            "Истек срок действия токена." \
            "Отправьте новый командой /token <jwt>"
        )
        return
    
    llm_request.delay(message.chat.id, message.text)
    await message.answer("Запрос принят")