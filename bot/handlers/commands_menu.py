import asyncio
import logging
from aiogram import Bot
from aiogram.types import BotCommand
from aiogram.exceptions import TelegramServerError, TelegramNetworkError

async def set_main_menu(bot: Bot) -> bool:
    commands = [
        BotCommand(command="/start", description="Главное меню"),
        BotCommand(command="buyvpn", description="Купить VPN 🛡"),
        BotCommand(command="myservices", description="Мои услуги 📦"),
        BotCommand(command="account", description="Аккаунт ⚙️"),
        BotCommand(command="aboutus", description="О нас ℹ️"),
    ]

    attempts = 3
    for attempt in range(1, attempts + 1):
        try:
            # Дадим больше времени Telegram на ответ
            await bot.set_my_commands(commands, request_timeout=30.0)
            return True
        except (TelegramServerError, TelegramNetworkError) as e:
            delay = min(2 ** attempt, 30)
            logging.warning(
                f"set_my_commands: временная ошибка (попытка {attempt}/{attempts}): {e}. Повтор через {delay}с"
            )
            await asyncio.sleep(delay)
        except Exception as e:
            logging.exception(f"set_my_commands: неожиданная ошибка: {e}")
            return False

    logging.error("set_my_commands: не удалось установить команды после всех попыток")
    return False
