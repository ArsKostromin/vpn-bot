from aiogram import Bot
from aiogram.types import BotCommand

async def set_main_menu(bot: Bot):
    commands = [
        BotCommand(command="buyvpn", description="Купить VPN 🛡"),
        BotCommand(command="buyproxy", description="Купить прокси 🔥"),
        BotCommand(command="myservices", description="Мои услуги 📦"),
        BotCommand(command="account", description="Аккаунт ⚙️"),
        BotCommand(command="topup", description="Пополнить баланс 💳"),
        BotCommand(command="help", description="Помощь 🆘"),
        BotCommand(command="reviews", description="Отзывы ⭐️"),
        BotCommand(command="aboutus", description="О нас ℹ️"),
        BotCommand(command="gift", description="Подарить другу 🎁"),
        BotCommand(command="partner", description="Партнёрка 🤝"),
        BotCommand(command="otherservices", description="Другие сервисы 🔗"),
        BotCommand(command="ourchannel", description="Наш канал 📣"),
    ]
    await bot.set_my_commands(commands)
