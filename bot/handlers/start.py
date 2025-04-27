from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot.db import get_user, create_user
from aiogram.filters import Command
from bot.keyboards.main_menu import inline_main_menu
from bot.keyboards.start_menu import inline_instruction_buttons
import aiohttp
from bot.services.user_service import register_user_via_api
from aiogram.enums import ParseMode


router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await process_start(message.from_user.id, message.from_user.username, message)

@router.callback_query(F.data == "start_from_button")
async def callback_start(callback: CallbackQuery):
    await process_start(callback.from_user.id, callback.from_user.username, callback.message)
    await callback.answer()

async def process_start(user_id: int, username: str, respond_to: Message):
    result = await register_user_via_api(user_id)

    if result:
        link_code, created = result

        if created:
            await respond_to.answer(
                text=(
                    f"✅Добро пожаловать в YouFast VPN™, {respond_to.from_user.full_name}!\n\n"
                    "🔧 Ваш VPN УЖЕ готов к работе и будет доступен **БЕСПЛАТНО три дня!**\n\n"
                    "📲 Установите приложение для вашей OS:\n\n"
                    "🍏 iOS: [neroVPN](https://)\n"
                    "🤖 Android: [neroVPN](https://)\n"
                    "🖥️ Windows: [neroVPN](https://)\n"
                    "🍏 MacOS: [neroVPN](https://)\n\n"
                    "🔗 Подключите VPN ключ в приложение (нажмите на текст ниже, чтобы скопировать):\n\n"
                    f"`{link_code}`\n\n"
                    "-----------------------------\n"
                    "💰 Наши цены после истечения пробной версии:\n"
                    "├ 1 мес: $5\n"
                    "├ 6 мес: $27 (-10%)\n"
                    "├ 1 год: $48.7 (-20%)\n"
                    "├ 3 года: $109.5 (-40%)"
                ),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=inline_instruction_buttons
            )
            return

    # Если пользователь уже есть или ошибка при регистрации
    await respond_to.bot.send_photo(
        chat_id=respond_to.chat.id,
        photo="https://play-lh.googleusercontent.com/BFkf2bgtxsCvsTnR2yw8yuWD3mgpThoyiRoBhoazTqFFMNOmdxGAAqS7vMATyNwelQ",
        caption=(
            "🔥 Наши серверы не имеют ограничений по скорости и трафику, VPN работает на всех устройствах, "
            "YouTube в 4K — без задержек!\n\n"
            "🔥 Максимальная анонимность и безопасность, которую не даст ни один VPN сервис в мире.\n\n"
            "✅ Наш канал: @meme17k"
        ),
        reply_markup=inline_main_menu,
        parse_mode=ParseMode.HTML
    )