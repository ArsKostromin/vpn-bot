import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from bot.handlers import start, vpn, my_services
from bot.config import load_config
from bot.db import init_db

# Настройка логгера
logging.basicConfig(level=logging.INFO)

# Конфигурация
config = load_config()

# Создание бота
bot = Bot(
    token=config.bot.token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

# Создание диспетчера
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(start.router)
dp.include_router(vpn.router)
dp.include_router(my_services.router)


async def main():
    await init_db(config.db.url)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
