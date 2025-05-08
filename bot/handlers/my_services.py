from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.exceptions import TelegramBadRequest
from bot.keyboards.my_services_keyboard import my_services_menu, not_subscription
from .start import process_start 
from bot.services.user_service import get_user_subscriptions, get_user_info
from bot.keyboards.back_menu import back_to_main_menu

router = Router()

@router.callback_query(F.data == "my_services")
async def my_services_screen(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username
    photo = FSInputFile("bot/media/telegram.jpg")

    subscriptions = await get_user_subscriptions(telegram_id=user_id)

    if not subscriptions:
        await callback.message.answer_photo(
            photo=photo,
            caption="У вас нет активных подписок. ❌",
            reply_markup=not_subscription
        )
    else:
        for sub in subscriptions:
            status = "✅ Активна" if sub['is_active'] else "❌ Неактивна"
            text = (
                f"<b>🔹 VPN:</b> {sub['vpn_type']}\n"
                f"<b>🔹 Длительность:</b> {sub['duration']}\n"
                f"<b>🔹 Цена:</b> {sub['price']}₽\n"
                f"<b>🔹 Статус:</b> {status}\n"
                f"<b>🔹 Начало:</b> {sub['start_date'][:10]}\n"
                f"<b>🔹 Окончание:</b> {sub['end_date'][:10]}\n\n"
                f"<b>Нажмите и удерживайте текст ниже, чтобы скопировать VLESS:</b>\n"
                f"<code>{sub['vless']}</code>"
            )

            await callback.message.answer(
                text,
                parse_mode="HTML",
                reply_markup=back_to_main_menu
            )

    await callback.answer()

    
@router.callback_query(F.data == "account")
async def profile_handler(callback: CallbackQuery):
    user_id = callback.from_user.id

    user_info = await get_user_info(telegram_id=user_id)

    if not user_info:
        await callback.message.answer("Не удалось получить информацию о вашем профиле. Попробуйте позже.")
        return

    balance = user_info.get('balance', 0)
    link_code = user_info.get('link_code', 'Нет')

    text = (
        f"💼 Ваш профиль:\n\n"
        f"▪️ Баланс: {balance}₽\n"
        f"▪️ реферальная ссылка: https://t.me/Anonixvpn_vpnBot?start={link_code}"
    )

    reply_markup = back_to_main_menu

    await callback.message.answer(text, reply_markup=reply_markup)
    await callback.answer()