from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_dialog import setup_dialogs

from hozbot.logger import logger
from hozbot.config import settings
from hozbot.database.engine import async_session_maker
from hozbot.keyboards.helper_menu import set_main_menu
from hozbot.handlers.user import router as user_router
from hozbot.handlers.user_dialogs import dialog_router
from hozbot.handlers.admin import admin_router
from hozbot.handlers.admin_panel import router as panel_router
from hozbot.middlewares.db import DataBaseSession

from redis.asyncio import Redis

logger.info("Starting bot")
redis = RedisStorage(
    redis=Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
    ),
    key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
)

storage = redis if settings.USE_REDIS else MemoryStorage()
bot = Bot(token=settings.TG_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher(storage=storage)

dp.callback_query.middleware(CallbackAnswerMiddleware())
dp.startup.register(set_main_menu)

# register_all_handlers(dp)


async def on_shutdown(bot):
    logger.info('Бот лег')


async def bot_main():
    try:
        dp.include_routers(admin_router,
                           panel_router,
                           user_router,
                           dialog_router,
                           )
        setup_dialogs(dp)
        dp.shutdown.register(on_shutdown)
        dp.update.middleware(DataBaseSession(session_pool=async_session_maker))
        await bot.delete_webhook(True)
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()
