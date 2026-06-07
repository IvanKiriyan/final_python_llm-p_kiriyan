import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.bot.dispatcher import bot, dp

@asynccontextmanager
async def lifespan(app: FastAPI):
    polling_task = asyncio.create_task(
        dp.start_polling(bot, handle_signals=False)
    )
    yield
    polling_task.cancel()
    try:
        await polling_task
    except asyncio.CancelledError:
        pass
    await dp.stop_polling()
    await bot.session.close()

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.APP_NAME}