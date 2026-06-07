import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from aiogram.types import Chat, Message, User

def make_message(user_id: int, text: str, chat_id: int | None = None) -> MagicMock:
    msg = MagicMock(spec=Message)
    msg.from_user = MagicMock(spec=User)
    msg.from_user.id = user_id
    msg.chat = MagicMock(spec=Chat)
    msg.chat.id = chat_id or user_id
    msg.text = text
    msg.answer = AsyncMock()
    return msg

@pytest.mark.asyncio
async def test_cmd_token_saves_to_redis(fake_redis, valid_token):
    from app.bot.handlers import cmd_token

    msg = make_message(user_id=100, text=f"/token {valid_token}")

    async def mock_get_redis():
        return fake_redis

    with patch("app.bot.handlers.get_redis", new=mock_get_redis):
        await cmd_token(msg)

    saved = await fake_redis.get("token:100")
    assert saved == valid_token
    msg.answer.assert_called_once()
    assert "сохран" in msg.answer.call_args.args[0].lower()

@pytest.mark.asyncio
async def test_cmd_text_no_token(fake_redis):
    from app.bot.handlers import cmd_text

    msg = make_message(user_id=200, text="Привет, бот")

    async def mock_get_redis():
        return fake_redis

    with (
        patch("app.bot.handlers.get_redis", new=mock_get_redis),
        patch("app.bot.handlers.llm_request") as mock_task,
    ):
        await cmd_text(msg)

    mock_task.delay.assert_not_called()
    msg.answer.assert_called_once()
    assert "токен" in msg.answer.call_args.args[0].lower()

@pytest.mark.asyncio
async def test_cmd_text_with_valid_token(fake_redis, valid_token):
    from app.bot.handlers import cmd_text

    await fake_redis.set("token:300", valid_token)
    msg = make_message(user_id=300, text="Расскажи про Python", chat_id=300)

    async def mock_get_redis():
        return fake_redis

    with (
        patch("app.bot.handlers.get_redis", new=mock_get_redis),
        patch("app.bot.handlers.llm_request") as mock_task,
    ):
        await cmd_text(msg)

    mock_task.delay.assert_called_once_with(300, "Расскажи про Python")
    msg.answer.assert_called_once()
    assert "принят" in msg.answer.call_args.args[0].lower()