from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot.keyboards.balance_menu import get_balance_menu
from bot.services.upbalance import create_payment_link

router = Router()

# Показываем меню пополнения
@router.callback_query(F.data == "balance_up")
async def balance_menu_callback(call: CallbackQuery):
    await call.message.answer(
        "Выберите сумму пополнения:",
        reply_markup=get_balance_menu()
    )
    await call.answer()

# Обрабатываем выбор суммы
@router.callback_query(F.data.startswith("topup_"))
async def process_topup(callback: CallbackQuery):
    amount_str = callback.data.split("_")[1]
    amount = int(amount_str)

    try:
        payment_link = await create_payment_link(telegram_id=callback.from_user.id, amount=amount)
        await callback.message.answer(f"Вот ваша ссылка для оплаты на {amount} ₽:\n{payment_link}")
        await callback.answer()
    except Exception as e:
        await callback.message.answer("Ошибка при создании платежа. Попробуйте позже.")
        await callback.answer()

# Обработка кнопки "Назад"
@router.callback_query(F.data == "back_to_menu")
async def back_to_main_menu(callback: CallbackQuery):
    await callback.message.answer("Вы вернулись в главное меню.")
    await callback.answer()
