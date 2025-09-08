from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.exceptions import TelegramBadRequest
from bot.keyboards.my_services_keyboard import my_services_menu, not_subscription, get_autorenew_keyboard
from .start import process_start 
from bot.services.user_service import get_user_subscriptions, get_user_info, toggle_autorenew
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
                f"<b>🔹 VPN:</b> {sub['vpn_type_display']}\n"
                f"<b>🔹 Цена:</b> {sub['price']}$\n"
                f"<b>🔹 Статус:</b> {status}\n"
                f"<b>🔹 Начало:</b> {sub['start_date'][:10]}\n"
                f"<b>🔹 Окончание:</b> {sub['end_date'][:10]}\n"
                f"<b>🔹 Автопродление:</b> {'Включено' if sub.get('auto_renew') else 'Выключено'}\n\n"
                f"<b>Нажмите и удерживайте текст ниже, чтобы скопировать VLESS:</b>\n"
                f"<code>{sub['vless']}</code>"
            )

            await callback.message.answer(
                text,
                parse_mode="HTML",
                reply_markup=get_autorenew_keyboard(sub['id'], sub.get('auto_renew', False))
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
    referrals_count = user_info.get('referrals_count', 0)

    text = (
        f"💼 Ваш профиль:\n\n"
        f"▪️ Баланс: {balance}$\n"
        f"▪️ Рефералов: {referrals_count}\n"
        f"▪️ Реферальная ссылка: https://t.me/Anonixvpn1Bot?start={link_code}"
    )

    reply_markup = back_to_main_menu

    await callback.message.answer(text, reply_markup=reply_markup, disable_web_page_preview=True)
    await callback.answer()

@router.callback_query(F.data.startswith("toggle_autorenew:"))
async def toggle_autorenew_handler(callback: CallbackQuery):
    subscription_id = int(callback.data.split(":")[1])
    user_id = callback.from_user.id
    result = await toggle_autorenew(subscription_id, user_id)
    if result is None:
        await callback.message.answer("Ошибка при изменении автопродления. Попробуйте позже.")
        await callback.answer()
        return
    auto_renew = result.get("auto_renew", False)
    await callback.message.edit_reply_markup(reply_markup=get_autorenew_keyboard(subscription_id, auto_renew))
    await callback.answer(f"Автопродление {'включено' if auto_renew else 'отключено'}.")