from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from states import CouponState
from bot.services.coupon import apply_coupon

router = Router()

# 1. Обработка нажатия кнопки "Ввести промокод"
@router.callback_query(F.data == "coupon")
async def ask_coupon(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите промокод:")
    await state.set_state(CouponState.waiting_for_code)
    await callback.answer()  # Убирает "часики"
    
# 2. Получение промокода от пользователя
@router.message(CouponState.waiting_for_code)
async def process_coupon(message: Message, state: FSMContext):
    code = message.text.strip()
    result = await apply_coupon(code, telegram_id=message.from_user.id)
    await message.answer(result)
    await state.clear()
