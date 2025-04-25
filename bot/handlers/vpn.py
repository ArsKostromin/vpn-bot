from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.states.vpn import BuyVPN
from bot.keyboards.vpn_menu import get_vpn_type_kb, get_duration_kb
from bot.services.buy_vpn import (
    get_vpn_types_from_api,
    get_durations_by_type_from_api,
    buy_subscription_api
)
from bot.handlers.start import process_start

router = Router()

@router.callback_query(F.data == "buy_vpn")
async def start_vpn_buying(callback: CallbackQuery, state: FSMContext):
    vpn_types = await get_vpn_types_from_api()
    await callback.message.answer("Выберите тип VPN:", reply_markup=get_vpn_type_kb(vpn_types))
    await state.set_state(BuyVPN.vpn_type)
    await callback.answer()  # закрыть "часики"

@router.callback_query(F.data.startswith("vpn_type:"))
async def select_duration(callback: CallbackQuery, state: FSMContext):
    vpn_type = callback.data.split(":")[1]
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
    duration = callback.data.split(":")[1]
    data = await state.get_data()
    vpn_type = data["vpn_type"]

    success, msg = await buy_subscription_api(
        telegram_id=callback.from_user.id,
        vpn_type=vpn_type,
        duration=duration
    )

    await callback.message.answer(msg)
    await state.clear()

    await process_start(
        user_id=callback.from_user.id,
        username=callback.from_user.username,
        respond_to=callback.message
    )
    await callback.answer()
