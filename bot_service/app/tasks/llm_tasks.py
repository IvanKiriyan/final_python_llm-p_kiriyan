import asyncio
import httpx
from app.infra.celery_app import celery_app
from app.core.config import settings
from app.services.openrouter_client import connection_openrouter

@celery_app.task(name="llm_request")
def llm_request(tg_chat_id: int, prompt: str) -> None: # получает айди чата и задачу для ллм
    asyncio.run(_process(tg_chat_id, prompt))

async def _process(tg_chat_id: int, prompt: str) -> None:
    try:
        text = await connection_openrouter(prompt)
    except Exception as e:
        text = f"Ошибка при подключении к модели: {e}"
    
    async with httpx.AsyncClient(timeout=30.0) as client: # отправляет обратно в чат тг
        await client.post(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": tg_chat_id, "text": text},
        )