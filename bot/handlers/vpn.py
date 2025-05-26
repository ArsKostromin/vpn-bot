from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.states.vpn import BuyVPN
from bot.keyboards.vpn_menu import (
    get_vpn_type_kb,
    get_duration_kb,
    get_insufficient_funds_kb,
    get_instruktion_kb,
    get_country_kb as get_country_kb_func,
    get_confirmation_kb,
)
from bot.services.buy_vpn import (
    get_vpn_types_from_api,
    get_durations_by_type_from_api,
    buy_subscription_api,
    build_tariff_showcase
)

router = Router()


@router.callback_query(F.data == "buy_vpn")
async def select_target(callback: CallbackQuery, state: FSMContext):
    vpn_types = await get_vpn_types_from_api()
    await callback.message.answer(
        text=(
            "Выберите VPN по цели использования или стране ⬇️\n\n"
            "⚠️ Вы получите VPN той страны, где мы гарантируем стабильную работу для выбранного направления.\n\n"
            "🧠 *Что значат «Одиночное» и «Двойное» шифрование?*\n"
            "— *Одиночное* шифрование — это стандартная защита и высокая скорость 🔓🚀\n"
            "— *Двойное* шифрование — повышенная анонимность за счёт маршрутизации через два узла, но скорость ниже 🛡️🔒\n\n"
            "Если вам нужна конкретная страна VPN – жмите «Выбрать по стране»."
        ),
        reply_markup=get_vpn_type_kb(vpn_types),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("vpn_type:"))
async def select_country_or_duration(callback: CallbackQuery, state: FSMContext):
    vpn_type = callback.data.split(":")[1]
    await state.update_data(vpn_type=vpn_type)

    if vpn_type == "country":
        await callback.message.answer(
            text="Выберите страну для VPN:",
            reply_markup=get_country_kb_func()
        )
    else:
        plans = await get_durations_by_type_from_api(vpn_type)

        if not plans:
            await callback.message.answer("❌ Нет доступных подписок.")
            await callback.answer()
            return

        text = build_tariff_showcase(title=callback.message.text or "Тарифы", plans=plans)

        await callback.message.answer(
            text=text,
            reply_markup=get_duration_kb([
                (p["duration"], str(p["price"]), p["duration_display"], p["discount_percent"])
                for p in plans
            ]),
            parse_mode="Markdown"
        )
        await state.set_state(BuyVPN.duration)

    await callback.answer()


@router.callback_query(F.data.startswith("target_country"))
async def select_duration_by_country(callback: CallbackQuery, state: FSMContext):
    durations_with_price = await get_durations_by_type_from_api("country")

    if not durations_with_price:
        await callback.message.answer("❌ Нет доступных подписок.")
        await callback.answer()
        return

    await callback.message.answer(
        text="Выберите тип подписки:",
        reply_markup=get_duration_kb(durations_with_price)
    )
    await state.set_state(BuyVPN.duration)

    await callback.answer()


@router.callback_query(F.data.startswith("duration:"))
async def show_confirmation(callback: CallbackQuery, state: FSMContext):
    duration = callback.data.split(":")[1]
    data = await state.get_data()
    vpn_type = data["vpn_type"]

    plans = await get_durations_by_type_from_api(vpn_type)
    selected = next((p for p in plans if p["duration"] == duration), None)

    if not selected:
        await callback.message.answer("❌ Такой подписки не существует.")
        await callback.answer()
        return

    await state.update_data(duration=duration)

    price = selected["discount_price"] if selected["discount_price"] else selected["price"]
    text = (
        f"🛒 *Вы выбрали:*\n"
        f"Тип: `{vpn_type}`\n"
        f"Срок: *{selected['duration_display']}*\n"
        f"Цена: *${price:.2f}*\n\n"
        f"✅ Нажмите *«Оплатить»*, чтобы оформить подписку."
    )

    await callback.message.answer(
        text=text,
        reply_markup=get_confirmation_kb(),
        parse_mode="Markdown"
    )
    await state.set_state(BuyVPN.confirmation)
    await callback.answer()


@router.callback_query(F.data == "confirm_payment")
async def complete_subscription(callback: CallbackQuery, state: FSMContext):
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


@router.callback_query(F.data == "cancel_payment")
async def cancel_subscription(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("❌ Покупка отменена.")
    await state.clear()
    await callback.answer()
