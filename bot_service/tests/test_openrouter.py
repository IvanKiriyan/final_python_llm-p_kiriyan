import httpx
import pytest
import respx
from app.services.openrouter_client import connection_openrouter

MOCK_RESPONSE = {
    "choices": [
        {"message": {"content": "Тестовый ответ от LLM"}}
    ]
}

@pytest.mark.asyncio
@respx.mock
async def test_connection_openrouter_success():
    route = respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
        return_value=httpx.Response(200, json=MOCK_RESPONSE)
    )

    result = await connection_openrouter("Тестовый вопрос")

    assert route.called
    assert result == "Тестовый ответ от LLM"

@pytest.mark.asyncio
@respx.mock
async def test_connection_openrouter_error():
    route = respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
        return_value=httpx.Response(500, text="Internal Server Error")
    )

    with pytest.raises(RuntimeError):
        await connection_openrouter("Тестовый вопрос")

    assert route.called