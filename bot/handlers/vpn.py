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
    get_target_vpn_kb as get_target_vpn_func,
)
from bot.services.buy_vpn import (
    get_vpn_types_from_api,
    get_durations_by_type_from_api,
    buy_subscription_api,
)

router = Router()

@router.callback_query(F.data == "buy_vpn1")
async def start_vpn_buying(callback: CallbackQuery, state: FSMContext):
    vpn_types = await get_vpn_types_from_api()
    description = (
        "🔒 <b>Одинарное шифрование (Solo VPN)</b>\n"
        "Трафик проходит через один VPN-сервер, шифруясь один раз (например, AES-256).\n\n"
        "🔐 <b>Двойное шифрование (Double VPN / Multi-hop)</b>\n"
        "Трафик последовательно шифруется на двух серверах, усиливая анонимность.\n\n"
        "Выберите тип VPN:"
    )
    await callback.message.answer(description, reply_markup=get_vpn_type_kb(vpn_types), parse_mode="HTML")
    await state.set_state(BuyVPN.vpn_type)
    await callback.answer()

@router.callback_query(F.data.startswith("vpn_type:"))
async def select_duration(callback: CallbackQuery, state: FSMContext):
    vpn_type = callback.data.split(":", 1)[1]
    await state.update_data(vpn_type=vpn_type)

    durations_with_price = await get_durations_by_type_from_api(vpn_type)
    if not durations_with_price:
        await callback.message.answer("❌ Нет доступных подписок для этого типа VPN.")
        await callback.answer()
        return

    await callback.message.answer(
        text="Выберите длительность подписки:",
        reply_markup=get_duration_kb(durations_with_price)
    )
    await state.set_state(BuyVPN.duration)
    await callback.answer()

@router.callback_query(F.data.startswith("duration:"))
async def complete_subscription(callback: CallbackQuery, state: FSMContext):
    duration = callback.data.split(":", 1)[1]
    data = await state.get_data()
    vpn_type = data.get("vpn_type")

    success, msg, vless = await buy_subscription_api(callback.from_user.id, vpn_type, duration)

    if not success and "недостаточно средств" in msg.lower():
        await callback.message.answer(
            "❌ Недостаточно средств для оформления подписки.",
            reply_markup=get_insufficient_funds_kb()
        )
        await callback.answer()
        return

    reply_markup = get_instruktion_kb if success and vless else None

    if vless:
        msg += (
            f"\n\n<b>Нажмите и удерживайте ниже, чтобы скопировать VLESS:</b>\n"
            f"<code>{vless}</code>\n\n"
            "Чтобы использовать его, скачайте приложение под вашу платформу."
        )

    await callback.message.answer(msg, parse_mode="HTML", reply_markup=reply_markup)
    await state.clear()
    await callback.answer()

@router.callback_query(F.data == "buy_vpn")
async def select_target(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text=(
            "Выберите VPN по цели использования или стране ⬇️\n\n"
            "⚠️ Вы получите VPN той страны, в которой мы гарантируем работу выбранного направления.\n\n"
            "Если нужна конкретная страна VPN – жмите «Выбрать по стране»."
        ),
        reply_markup=get_target_vpn_func
    )
    await callback.answer()

@router.callback_query(F.data == "country")
async def select_country(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text=(
            "Выберите страну для вашего VPN ⬇️\n\n"
            "⚠️ Не используйте страновой VPN для торрентов – выберите цель использования.\n\n"
            "⛔️ Мы НЕ гарантируем, что ваш Instagram будет работать в России с российским IP 😄"
        ),
        reply_markup=get_country_kb_func()
    )
    await callback.answer()


# Универсальный обработчик для целей: соцсети, торрент, двойной, страна
TARGETS = {
    "target:social": ("solo", "YouTube и соцсети"),
    "target:torrent": ("solo", "торрентов"),
    "target:double": ("double", "двойным шифрованием"),
    "target:country": ("solo", "по стране"),
}

for target_key, (vpn_type_val, label) in TARGETS.items():
    @router.callback_query(F.data == target_key)
    async def _(callback: CallbackQuery, state: FSMContext, vpn_type=vpn_type_val, label=label):
        await state.update_data(vpn_type=vpn_type)

        durations_with_price = await get_durations_by_type_from_api(vpn_type)
        if not durations_with_price:
            await callback.message.answer(f"❌ Нет доступных подписок для {label}.")
            await callback.answer()
            return

        await callback.message.answer(
            text=f"Выберите длительность подписки для {label}:",
            reply_markup=get_duration_kb(durations_with_price)
        )
        await state.set_state(BuyVPN.duration)
        await callback.answer()
