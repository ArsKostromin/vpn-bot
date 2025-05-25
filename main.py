import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from bot.handlers import start, vpn, my_services, balance, coupon, menu_callbacks
from bot.handlers.commands_menu import set_main_menu
from bot.config import load_config
from bot.db import init_db
from bot.notify_server import run_aiohttp_server  # 👈 импорт aiohttp-сервера

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
dp.include_router(balance.router)
dp.include_router(menu_callbacks.router)
dp.include_router(coupon.router)

async def main():
    await init_db(config.db.url)
    await set_main_menu(bot)

    # Запуск aiohttp и polling одновременно
    await asyncio.gather(
        run_aiohttp_server(bot),     # 🚀 aiohttp сервер
        dp.start_polling(bot)        # 🟢 запуск бота
    )

if __name__ == "__main__":
    asyncio.run(main())
