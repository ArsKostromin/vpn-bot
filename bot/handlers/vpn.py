# Импорты из aiogram: маршрутизатор, фильтры, типы и состояния
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

# Импорт состояний FSM и нужных клавиатур
from bot.states.vpn import BuyVPN
from bot.keyboards.vpn_menu import (
    get_vpn_type_kb,              # Кнопки выбора типа VPN
    get_duration_kb,              # Кнопки выбора длительности
    get_insufficient_funds_kb,    # Кнопки при нехватке средств
    get_instruktion_kb,           # Кнопки после покупки
    get_country_kb as get_country_kb_func,  # Кнопки выбора страны
)

# Импорт функций для получения данных от API
from bot.services.buy_vpn import (
    get_vpn_types_from_api,           # Получение всех типов VPN с бэкенда
    get_durations_by_type_from_api,  # Получение цен и длительностей
    buy_subscription_api              # Покупка подписки
)

# Создаём роутер для регистрации хендлеров
router = Router()

# Хендлер: старт выбора VPN
@router.callback_query(F.data == "buy_vpn")
async def select_target(callback: CallbackQuery, state: FSMContext):
    vpn_types = await get_vpn_types_from_api()

    await callback.message.answer(
        text=(
            "Выберите VPN по цели использования или стране ⬇️\n\n"
            "⚠️ Вы получите VPN той страны, в которой мы гарантируем работу выбранного вами направления.\n\n"
            "Если же вам нужна конкретная страна VPN – жмите «Выбрать по стране»."
        ),
        reply_markup=get_vpn_type_kb(vpn_types)
    )
    await callback.answer()


# Хендлер: обработка выбора цели/типа VPN
@router.callback_query(F.data.startswith("vpn_type:"))
async def select_country_or_duration(callback: CallbackQuery, state: FSMContext):
    vpn_type = callback.data.split(":")[1]
    await state.update_data(vpn_type=vpn_type)

    if vpn_type == "country":
        await callback.message.answer(
            text="Выберите страну для VPN:",
            reply_markup=get_country_kb_func()  # каждая кнопка — страна
        )
    else:
        durations_with_price = await get_durations_by_type_from_api(vpn_type)

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


# Хендлер: покупка подписки после выбора длительности
@router.callback_query(F.data.startswith("duration:"))
async def complete_subscription(callback: CallbackQuery, state: FSMContext):
    duration = callback.data.split(":")[1]
    data = await state.get_data()
    vpn_type = data["vpn_type"]

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
            f"\n\n<b>Нажмите и удерживайте ниже, чтобы скопировать VLESS:</b>\n"
            f"<code>{vless}</code>\n\n"
            "Чтобы его использовать, скачайте приложение под вашу платформу."
        )
        reply_markup = get_instruktion_kb()

    await callback.message.answer(msg, parse_mode="HTML", reply_markup=reply_markup)
    await state.clear()
    await callback.answer()
    
    
@router.callback_query(F.data.startswith("target_country"))
async def select_duration_by_country(callback: CallbackQuery, state: FSMContext):
    if not durations_with_price:
        await callback.message.answer("❌ Нет доступных подписок по выбранной стране.")
        await callback.answer()
        return

    durations_with_price = await get_durations_by_type_from_api('country')

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