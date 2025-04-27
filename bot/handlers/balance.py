from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot.keyboards.balance_menu import get_balance_menu, start_balance
from bot.services.upbalance import create_payment_link, create_crypto_payment
import traceback

router = Router()



@router.callback_query(F.data == "balance_up")
async def balance_up_callback(call: CallbackQuery):
    await call.bot.send_photo(
        chat_id=call.message.chat.id,
        photo="https://play-lh.googleusercontent.com/BFkf2bgtxsCvsTnR2yw8yuWD3mgpThoyiRoBhoazTqFFMNOmdxGAAqS7vMATyNwelQ",
        caption="🔥 Выберите крипту или Робокассу",
        reply_markup=start_balance,
    )


# Показываем меню пополнения
@router.callback_query(F.data == "robokassa")
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



#crypt

# Когда пользователь нажимает "Пополнить баланс"
@router.callback_query(F.data == "cryptobot")
async def balance_up_start(call: CallbackQuery):
    await call.message.answer(
        "💵 Выберите сумму для пополнения:",
        reply_markup=get_balance_menu()
    )

# Когда пользователь выбрал сумму
@router.callback_query(F.data.startswith("balance_amount_"))
async def create_payment(call: CallbackQuery):
    amount = int(call.data.split("_")[-1])
    telegram_id = call.from_user.id

    try:
        payment_url = await create_crypto_payment(telegram_id, amount)
        await call.message.answer(
            f"🧾 Оплата на сумму {amount} ₽ создана!\n\n"
            f"👉 Оплатить можно по ссылке: {payment_url}"
        )
    except Exception as e:
        # Отправить короткое сообщение пользователю
        await call.message.answer(f"❌ Ошибка при создании платежа. Попробуйте позже.")
        # А в логи сохранить полную трассировку
        import logging
        logging.error(f"Ошибка при создании платежа для {telegram_id}: {e}")
        logging.error(traceback.format_exc())