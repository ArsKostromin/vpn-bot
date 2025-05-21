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
    get_target_vpn as get_target_vpn_func
)
from bot.services.buy_vpn import (
    get_vpn_types_from_api,
    get_durations_by_type_from_api,
    buy_subscription_api
)

router = Router()

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


# @router.callback_query(F.data == "buy_vpn1")
# async def start_vpn_buying(callback: CallbackQuery, state: FSMContext):
#     vpn_types = await get_vpn_types_from_api()

#     description = (
#         "🔒 <b>Одинарное шифрование (Solo VPN)</b>\n"
#         "Трафик проходит через один VPN-сервер, шифруясь один раз (например, AES-256). "
#         "Достаточно для защиты в публичных сетях и обхода блокировок.\n\n"
#         "🔐 <b>Двойное шифрование (Double VPN / Multi-hop)</b>\n"
#         "Трафик последовательно шифруется на двух серверах, усиливая анонимность. "
#         "Подходит для максимальной конфиденциальности.\n\n"
#         "Выберите тип VPN:"
#     )

#     await callback.message.answer(description, reply_markup=get_vpn_type_kb(vpn_types), parse_mode="HTML")
#     await state.set_state(BuyVPN.vpn_type)
#     await callback.answer()


@router.callback_query(F.data.startswith("vpn_type:"))
async def select_duration(callback: CallbackQuery, state: FSMContext):
    vpn_type = callback.data.split(":")[1]
    await state.update_data(vpn_type=vpn_type)

    # получаем список длительностей с ценами
    durations_with_price = await get_durations_by_type_from_api(vpn_type)

    if not durations_with_price:
        await callback.message.answer("❌ Нет доступных подписок.")
        await callback.answer()
        return

    # отправляем клавиатуру с вариантами длительности
    await callback.message.answer(
        text="Выберите тип подписки:",
        reply_markup=get_duration_kb(durations_with_price)
    )

    # переводим в состояние выбора длительности
    await state.set_state(BuyVPN.duration)
    await callback.answer()


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
            "чтобы его использовать скачайте приложение под вашу платформу"
        )
        reply_markup = get_instruktion_kb

    await callback.message.answer(msg, parse_mode="HTML", reply_markup=reply_markup)
    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "country")
async def select_country(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text=(
            "Выберите страну для вашего VPN ⬇️\n\n"
            "⚠️ Если вам нужен VPN для соцсетей или торрентов – вернитесь назад и выберите цель использования. "
            "Ни в коем случае не используйте просто страновой VPN для скачивания с торрентов!\n\n"
            "⛔️ Выбирая страну самостоятельно, мы НЕ гарантируем что ваш инстаграм будет работать в России с российского IP 😄"
        ),
        reply_markup=get_country_kb_func()
    )
    await callback.answer()



@router.callback_query(F.data == "target:social")
async def select_duration_social(callback: CallbackQuery, state: FSMContext):
    vpn_type = "socials"
    await state.update_data(vpn_type=vpn_type)

    durations_with_price = await get_durations_by_type_from_api(vpn_type)

    if not durations_with_price:
        await callback.message.answer("❌ Нет доступных подписок для YouTube и соцсетей.")
        await callback.answer()
        return

    await callback.message.answer(
        text="Выберите длительность подписки для YouTube и соцсетей:",
        reply_markup=get_duration_kb(durations_with_price)
    )
    await state.set_state(BuyVPN.duration)
    await callback.answer()
    
    
@router.callback_query(F.data == "target:torrent")
async def select_duration_social(callback: CallbackQuery, state: FSMContext):
    vpn_type = "torrents"
    await state.update_data(vpn_type=vpn_type)

    durations_with_price = await get_durations_by_type_from_api(vpn_type)

    if not durations_with_price:
        await callback.message.answer("❌ Нет доступных подписок для YouTube и соцсетей.")
        await callback.answer()
        return

    await callback.message.answer(
        text="Выберите длительность подписки для torrent:",
        reply_markup=get_duration_kb(durations_with_price)
    )
    await state.set_state(BuyVPN.duration)
    await callback.answer()


@router.callback_query(F.data == "target:double")
async def select_duration_double(callback: CallbackQuery, state: FSMContext):
    vpn_type = "secure"
    await state.update_data(vpn_type=vpn_type)

    durations_with_price = await get_durations_by_type_from_api(vpn_type)

    if not durations_with_price:
        await callback.message.answer("❌ Нет доступных подписок для Double VPN.")
        await callback.answer()
        return

    await callback.message.answer(
        text="Выберите длительность подписки с двойным шифрованием:",
        reply_markup=get_duration_kb(durations_with_price)
    )
    await state.set_state(BuyVPN.duration)
    await callback.answer()


@router.callback_query(F.data == "target:country")
async def select_duration_social(callback: CallbackQuery, state: FSMContext):
    vpn_type = "country"
    await state.update_data(vpn_type=vpn_type)

    durations_with_price = await get_durations_by_type_from_api(vpn_type)

    if not durations_with_price:
        await callback.message.answer("❌ Нет доступных подписок для YouTube и соцсетей.")
        await callback.answer()
        return

    await callback.message.answer(
        text="Выберите длительность подписки:",
        reply_markup=get_duration_kb(durations_with_price)
    )
    await state.set_state(BuyVPN.duration)
    await callback.answer()
