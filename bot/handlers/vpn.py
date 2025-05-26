from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from bot.states.vpn import BuyVPN
from bot.keyboards.vpn import get_vpn_type_kb, get_duration_kb, get_insufficient_funds_kb, get_instruktion_kb
from bot.services.vpn import get_vpn_types_from_api, get_durations_by_type_from_api, buy_subscription_api

router = Router()

@router.callback_query(F.data == "buy_vpn")
async def choose_vpn_type(callback: CallbackQuery, state: FSMContext):
    vpn_types = await get_vpn_types_from_api()
    await state.set_state(BuyVPN.vpn_type)
    await callback.message.edit_text(
        "Выберите тип VPN:",
        reply_markup=get_vpn_type_kb(vpn_types)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("vpn_type:"))
async def choose_duration(callback: CallbackQuery, state: FSMContext):
    vpn_type = callback.data.split(":")[1]
    await state.update_data(vpn_type=vpn_type)

    durations = await get_durations_by_type_from_api(vpn_type)
    await state.set_state(BuyVPN.duration)
    await callback.message.edit_text(
        f"Вы выбрали <b>{vpn_type}</b> VPN.\nТеперь выберите длительность подписки:",
        reply_markup=get_duration_kb(durations),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("duration:"))
async def preview_subscription(callback: CallbackQuery, state: FSMContext):
    duration = callback.data.split(":")[1]
    data = await state.get_data()
    vpn_type = data["vpn_type"]

    plans = await get_durations_by_type_from_api(vpn_type)
    plan = next((p for p in plans if p["duration"] == duration), None)

    if not plan:
        await callback.message.answer("❌ Ошибка при получении тарифа.")
        await callback.answer()
        return

    await state.update_data(duration=duration, plan=plan)

    price = plan["discount_price"] or plan["price"]
    percent = plan["discount_percent"]
    label = plan["duration_display"]
    price_line = f"${price:.2f}" + (f" (скидка -{percent}%)" if percent else "")

    text = (
        f"✅ <b>Подтверждение покупки</b>\n\n"
        f"🔹 <b>Тип VPN:</b> {vpn_type.capitalize()}\n"
        f"🕒 <b>Срок:</b> {label}\n"
        f"💵 <b>Стоимость:</b> {price_line}\n\n"
        f"🔗 После оплаты подписка активируется автоматически."
    )

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 Оплатить", callback_data="confirm_buy")],
            [InlineKeyboardButton(text="❌ Отменить платёж", callback_data="cancel_buy")]
        ]
    )

    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await state.set_state(BuyVPN.confirmation)
    await callback.answer()


@router.callback_query(F.data == "confirm_buy")
async def confirm_buy(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    vpn_type = data["vpn_type"]
    duration = data["duration"]

    success, msg, vless = await buy_subscription_api(
        telegram_id=callback.from_user.id,
        vpn_type=vpn_type,
        duration=duration
    )

    if not success and "недостаточно средств" in msg.lower():
        await callback.message.answer(
            text="❌ Недостаточно средств для оформления подписки.",
            reply_markup=get_insufficient_funds_kb()
        )
        await callback.answer()
        return

    reply_markup = None
    if success and vless:
        msg += (
            f"\n\n<b>Нажмите, чтобы скопировать VLESS:</b>\n"
            f"<code>{vless}</code>\n\n"
            "Чтобы его использовать, скачайте приложение под вашу платформу."
        )
        reply_markup = get_instruktion_kb()

    await callback.message.answer(msg, parse_mode="HTML", reply_markup=reply_markup)
    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "cancel_buy")
async def cancel_buy(callback: CallbackQuery, state: FSMContext):
    vpn_types = await get_vpn_types_from_api()
    await callback.message.answer("❌ Покупка отменена.", reply_markup=get_vpn_type_kb(vpn_types))
    await state.clear()
    await callback.answer()
