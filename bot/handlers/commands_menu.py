from aiogram import Bot
from aiogram.types import BotCommand

async def set_main_menu(bot: Bot):
    commands = [
        BotCommand(command="buyvpn", description="Купить VPN 🛡"),
        BotCommand(command="myservices", description="Мои услуги 📦"),
        BotCommand(command="account", description="Аккаунт ⚙️"),
        BotCommand(command="aboutus", description="О нас ℹ️"),
    ]
    await bot.set_my_commands(commands)
